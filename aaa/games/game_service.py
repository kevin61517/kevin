"""
    GameService
    ~~~~~~~~~~~~
    游戏转账订单状态机

                    +---------------+
                    |    pending    |
                    +------+--------+
                           |
                           v
                    +------+-------+
                    |   scheduled  |
                    +------+-------+
                      |   ack   |
        +-------------+    |    +-------------+
        |  succeeded  +<---+--->+    failure  |
        +-+-----------+         +------+------+
          |                            |
          |                            v
          |                     +------+------+
          |                     |   reversed  |
          |                     +------+------+
          |                            |
          |     +---------------+      |
          +---->+   completed   +<-----+
                +---------------+

"""

import asyncio
import typing
from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from functools import wraps

import attr

from libs.sanic_limiter import RateLimitExceeded
from rpc.server import models
from rpc.server.db import scope_session
from rpc.server.executor import run_in_thread
from rpc.server.models.player import async_get_player, PlayerNotFound, async_get_real_name
from rpc.server.objects import Game, Player, Launch, User, GameTransfer
from rpc.server.run import shutdown_waits_for
from rpc.server.services.game.history import history
from rpc.server.services.game.interface import PlatformService
from rpc.server.services.game.fsm import GameTransferIn, GameTransferOut, GameTransferOutWithLaunch
from rpc.server.services.game.config import config
from rpc.server.helpers import json_loads, json_dumps
from rpc.server.core import redis
from rpc.logger import get_logger
from rpc.utils import to_decimal, cached_property
from spinach import exceptions
from spinach.constants import LAUNCH_CONTAIN_TRANSFER, LAUNCH_WITH_WALLET, DISABLED_PLATFORMS, AGIN_WALLET, IG_WALLET

logger = get_logger(__name__)

_MIN_AMOUNT = Decimal('0')


async def delay_wrapper(delay: int, coro: typing.Coroutine):
    await asyncio.sleep(delay)
    return await coro


def protect_transfer(user_or_player, prefix='_tt', expire=60):
    """
    保护游戏转账，确保同时只有一笔交易进行
    @param user_or_player:
    @param prefix: 锁前缀
    @param expire: 锁自动过期时间
    @return:
    """

    def _(coro):
        @wraps(coro)
        async def __(*args, **kwargs):
            user_id = kwargs[user_or_player].user_id
            name = f'{prefix}:{user_id}'
            ok = await redis.set(name, value=1, expire=expire, exist='SET_IF_NOT_EXIST')
            if ok:
                try:
                    return await coro(*args, **kwargs)
                finally:
                    await redis.delete(name)
            raise exceptions.PlatformTransferSystemBusy("已经有一笔交易正在进行，请稍后重试.")

        return __

    return _


@attr.s(slots=True)
class State:
    ban_transfer_set = attr.ib(type=set, default=set())
    platform_status = attr.ib(type=dict, default={})
    ban_wallet_set = attr.ib(type=set, default=set())

    def update_ban_transfer_set(self, user_id: str, method='add'):
        """更新禁止转账用户的集合"""
        if method == 'add':
            self.ban_transfer_set.add(user_id)
        elif method == 'remove':
            self.ban_transfer_set.discard(user_id)

    def is_ban_transfer_user(self, user_id) -> bool:
        return str(user_id) in self.ban_transfer_set

    def update_ban_wallet_set(self, user_id: str, method='add'):
        """更新禁止随身钱包的集合"""
        if method == 'add':
            self.ban_wallet_set.add(user_id)
        elif method == 'remove':
            self.ban_wallet_set.discard(user_id)

    def is_ban_wallet_user(self, user_id) -> bool:
        return str(user_id) in self.ban_wallet_set

    async def update_platform_status(self, platforms: list):
        """更新平台的维护状态"""
        platform_infos = await redis.mget(*[f'conf:{platform}' for platform in platforms])
        status = {"maintain": False, "maintain_end": "", "maintain_start": ""}
        for platform, data in dict(zip(platforms, platform_infos)).items():
            if data is not None:
                status = {key: value for key, value in json_loads(data).items() if key in
                          ['maintain_start', 'maintain_end', 'maintain']}
            status["platform"] = platform
            self.platform_status[platform] = status.copy()

    async def init(self):
        self.ban_transfer_set = set(await redis.smembers('ban:transfer'))
        self.ban_wallet_set = set(await redis.smembers('ban:wallet'))

        await self.update_platform_status(list(game_service._registry.keys()))


class GameService:
    """ 游戏服务，采用插件设计模式来进行统一管理游戏平台服务 """

    _registry: dict = {}
    state = State()

    def init_app(self, **kwargs):
        for kls in PlatformService.__subclasses__():
            name = kls.__name__
            if config.has(name):
                self.register(name, kls.from_config(config.get(name)))

    def register(self, name: str, service: PlatformService):
        """注册游戏服务"""
        self._registry[name] = service
        for alias in service.aliases:
            self._registry[alias] = service

        logger.info('game.register', service=name, aliases=service.aliases)

    def has(self, name):
        return name in self._registry

    def get_service(self, name, raise_on_error=True, check=True, init_games_mapping=False) -> PlatformService:
        """
        获取 PlatformService 实例
        :param name: 平台名称
        :param raise_on_error: 不存在该服务是否需要报错
        :param check: 是否检查在维护状态
        :param init_games_mapping: 是否需要初始化mapping -> for 注單
        :return:
        """
        s: PlatformService = self._registry.get(name)
        if s is None:
            if raise_on_error:
                raise exceptions.ServiceNotImplementedError(f"游戏平台 {name} 不支持")
            return None
        if check:
            self.check_service_status(name=name)
        if s.NEED_INIT_GAMES_MAPPING and init_games_mapping:
            self._init_games_mapping(s)
        return s

    @staticmethod
    def _init_games_mapping(service: PlatformService):
        """初始化遊戲名稱 MAPPING Example -> {'7850_1001_1002': '特工简·布隆德最大音量'}
        2022-12-29: 目前只支持Slot。
        """
        print('== 初始化電子遊戲對應表 ==')
        platform_names: list = [service.__class__.__name__, f'{service.__class__.__name__}Slot']
        with scope_session() as session:
            games_ = session.query(
                models.Game.code,
                models.Game.name
            ).filter(
                models.Game.platform.in_(platform_names)
            )
            service.GAMES.update({game.name: game.code for game in games_})

    def check_service_status(self, name):
        """
        check to see service under scheduled maintenance or not
        :param name:
        :return:
        """
        data = self.state.platform_status.get(name, {})
        if data.get('maintain', False):
            # TODO dead at here
            raise exceptions.PlatformMaintaining(payload=data)

    @property
    def services(self) -> typing.List[PlatformService]:
        """枚举所有游戏服务"""
        for service in self._registry.values():
            yield service

    @cached_property
    def all_wallets(self):
        """枚举所有钱包"""
        return {s.platform for s in self.services}

    async def close(self):
        """关闭服务"""
        for service in self.services:
            await service.close()

    async def launch(self, player: Player, game: Game, **kwargs) -> Launch:
        """
        启动游戏
        @param player:
        @param game:
        @return:
        """
        s = self.get_service(game.platform)

        if player.is_guest and not s.has_demo(game=game):
            raise exceptions.DemoNotSupported("游戏不支持试玩")

        amount = to_decimal(game.extra.get('amount', '0'))
        if s.LAUNCH_CONTAIN_TRANSFER and (not LAUNCH_WITH_WALLET) and LAUNCH_CONTAIN_TRANSFER and amount > 0:
            fsm = await self.launch_with_transfer(player=player, game=game, amount=amount, **kwargs)
            transfer = fsm.transfer
            error = fsm.error
            launch = fsm.launch
            self.on_transfer_completed(transfer=transfer,
                                       player=player,
                                       raise_on_failed=(fsm.launch is None),
                                       error=error)
        else:
            launch = await s.launch(player, game, **kwargs)

        if launch is None:
            raise exceptions.GameLaunchFailed()
        launch.game = game.game
        launch.platform = game.platform
        launch.demo = player.is_guest

        s.post_launch(player=player, game=game, launch=launch)
        history.push(player, platform=s.platform, game=game)
        return launch

    @protect_transfer(user_or_player='player')
    async def launch_with_transfer(self, player: Player, game: Game, amount, client_ip='127.0.0.1',
                                   **kwargs) -> GameTransferOutWithLaunch:
        """
        KY，LC，LY棋牌启动游戏是支持带分启动的，这里单独实现一个游戏转账状态机器加启动对象
        @param player:
        @param game:
        @param client_ip: 客户端IP
        @param amount: 转账金额
        @param kwargs:
        @return:
        """
        s = self.get_service(game.platform)
        transfer = GameTransfer(platform=s.platform,
                                username=player.username,
                                direction='OUT',
                                order_no=s.new_billno(player=player),
                                client_ip=client_ip,
                                amount=amount,
                                user_id=player.user_id,
                                real_name=player.real_name)
        fsm = GameTransferOutWithLaunch(player=player, service=s, transfer=transfer, game=game, **kwargs)
        fsm.initial(fsm.states.PENDING)
        try:
            await shutdown_waits_for(fsm.start())
        except asyncio.CancelledError:
            logger.warn('fsm.cancelled',
                        platform=transfer.platform,
                        order_no=transfer.order_no,
                        status=transfer.status,
                        direction=transfer.direction,
                        username=transfer.username,
                        user_id=transfer.user_id,
                        amount=transfer.amount)
        return fsm

    async def launch_with_wallet(self, player: Player, game: Game, client_ip='127.0.0.1', **kwargs):
        """
        试玩用户不执行转账操作
        若启动平台和上次相同，则只闪入当前钱包余额到第三方
        若和上次启动平台不同，则先将其他平台(不包含需启动平台）闪入钱包， 然后再闪入第三方
        中心钱包余额为0时，不能抛异常终端游戏启动
        @param player:
        @param game:
        @param client_ip: 客户端IP
        @param kwargs:
        @return:
        """
        if not player.is_guest:
            print('== 正式用戶 ==')
            plats = await history.get_last_platform(player, count=3)
            print('plats===>', plats)
            last_platform = plats[0] if plats else ""
            print('上一個台子：', last_platform)
            platform = game.platform
            print('當前台子：', platform)

            last_platform_alias = self.get_last_platform_alias(last_platform)
            print('11111')

            if last_platform and last_platform != platform and (platform not in last_platform_alias):
                print('22222---transfer_in')
                players = await self.get_players(user_id=player.user_id)
                tasks = [
                    self._transfer_in(player=p, platform=p.platform, client_ip=client_ip)
                    for p in players if p.platform != platform and p.platform in plats
                ]
                await asyncio.gather(*tasks, return_exceptions=True)
                print('33333')
            try:
                print('44444---transfer_out')
                await self.transfer_out(player=player, platform=game.platform, client_ip=client_ip)
                print('55555')
            except exceptions.InSufficientMoney as e:
                logger.warn('player.launch_with_wallet', user_id=player.user_id, client_ip=client_ip)
        print('66666')
        launch = await self.launch(player, game, client_ip=client_ip, **kwargs)
        print('77777')
        return launch

    def get_last_platform_alias(self, last_platform: str) -> typing.List:
        last_platform_alias = []
        if last_platform:
            if last_platform in AGIN_WALLET:
                return AGIN_WALLET

            if last_platform in IG_WALLET:
                return IG_WALLET

            s = self.get_service(last_platform, raise_on_error=False, check=False)
            last_platform_alias = s.aliases if s else []

        return last_platform_alias

    async def create_player(self, user: User, platform: str, **kwargs) -> typing.Tuple[Player, bool]:
        """
        get or create player
        @param user:
        @param platform: MGSlot -> MG
        @param kwargs:
        @return:
        """
        print('== 我在這裡 ==')
        s = self.get_service(platform)  # -> 繼承 PlatformService interface 的遊戲實例物件
        print('== 完成 ==')
        try:
            player = await async_get_player(user_id=user.user_id, platform=s.platform)
            print('==== has player ====')
            print('player===>', player)
            return player, False
        except PlayerNotFound:
            print('==== new player ====')
            player = await s.create_player(user, **kwargs)
            await models.Player.async_upsert(player)
            # patch missing player.real_name
            player.real_name = await async_get_real_name(user.user_id)
            logger.info('game.player_created', player=player, platform=platform, user=user)
            return player, True

    async def query_balance(self, player: Player) -> dict:
        s = self.get_service(player.platform)
        result = await s.query_balance(player)
        result = max(result.quantize(Decimal('.01'), rounding=ROUND_DOWN), _MIN_AMOUNT)
        self._update_wallet(player, balance=result)
        return {'result': result, 'platform': player.platform}

    def _update_wallet(self, player: Player, balance: Decimal):
        """更新玩家钱包余额"""
        fut = redis.hset(f'wallets:{player.user_id}', field=player.platform, value=str(balance))
        asyncio.ensure_future(fut)

    def update_wallet(self, player: Player, delay=0):
        """异步刷新玩家钱包余额"""
        if delay > 0:
            fut = delay_wrapper(delay, self.query_balance(player))
        else:
            fut = self.query_balance(player)
        asyncio.ensure_future(fut)

    async def my_wallets(self, user: User, u_plat: int = None):
        """会员钱包余额"""
        user_balance = await self.get_user_balance(user.user_id)
        data = await redis.hgetall(f'wallets:{user.user_id}') or {}
        extra_disabled = []
        if u_plat is not None:
            zutou = 15
            extra_disabled.append('OBSport' if u_plat == zutou else 'ZutouSport')
        r = [{'platform': k, 'result': data.get(k, '0')}
             for k in self.all_wallets if k not in DISABLED_PLATFORMS + extra_disabled]
        r.append({'platform': '', 'result': user_balance['available_balance']})
        return r

    def merge_players(self, players: typing.List[Player]) -> typing.List[Player]:
        """平台存在别名共用一个钱包的平台, 我们合并这些玩家账号 """
        return [player for player in players if player.platform in self.all_wallets]

    async def get_players(self, user_id: int, merge=True) -> typing.List[Player]:
        """
        获取会员所有的玩家对象
        :param user_id:  会员ID
        :param merge: 是否合并同一个平台的玩家
        :return:
        """
        players = await models.Player.async_filter_by(user_id=user_id)
        if merge:
            return self.merge_players(players)
        return players

    async def query_balance_all(self, user: User) -> typing.List:
        """
        查询所有玩家所有平台余额

        使用 players 表来获取他所有第三方平台资金账户
        @param user:
        @return:
        """

        players = await self.get_players(user_id=user.user_id)
        tasks = [self.query_balance(player=p) for p in players]
        logger.debug('transfer.query_balance_all', tasks=len(tasks), user=user.user_id)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # silent ignore errors here
        results = [r for r in results if not isinstance(r, Exception)]
        logger.info('query_balance_all', user_id=user.user_id, tasks=len(tasks), success=len(results),
                    failed=len(tasks) - len(results))
        return results

    @protect_transfer(user_or_player='user')
    async def transfer_p2p(self,
                           *,
                           user: User,
                           src: str,
                           dst: str,
                           amount: Decimal,
                           client_ip="127.0.0.1") -> typing.Tuple[GameTransfer, GameTransfer]:
        """P2P 转账"""
        t1 = None
        t2 = None
        if src:
            player, _ = await self.create_player(user, platform=src)
            t1 = await self.transfer(player, platform=src, amount=amount, direction='IN', client_ip=client_ip)

        if dst:
            player, _ = await self.create_player(user, platform=dst)
            t2 = await self.transfer(player, platform=dst, amount=amount, direction='OUT', client_ip=client_ip)

        return t1, t2

    @protect_transfer(user_or_player='player')
    async def transfer_in(self, *, player: Player, platform, client_ip='127.0.0.1', **kwargs) -> GameTransfer:
        return await self._transfer_in(player=player, platform=platform, client_ip=client_ip, **kwargs)

    async def _transfer_in(self, player: Player, platform, client_ip='127.0.0.1', **kwargs) -> GameTransfer:
        """一键闪入平台"""
        r = await self.query_balance(player)
        balance = r['result']
        return await self.transfer(player,
                                   platform=platform,
                                   amount=balance,
                                   direction='IN',
                                   client_ip=client_ip,
                                   **kwargs)

    @run_in_thread
    def get_user_balance(self, user_id) -> dict:
        """
        玩家所有余额
        @param user_id:
        @return:
        """
        with scope_session() as session:
            r = session.query(models.Account.balance, models.Account.bonus, models.Account.credits) \
                .filter_by(user_id=user_id) \
                .one()
            return {
                'available_balance': r.balance + r.bonus,
                'bonus': r.bonus,
                'balance': r.balance,
                'credits': r.credits
            }

    @protect_transfer(user_or_player='player')
    async def transfer_out(self, *, player: Player, platform, client_ip='127.0.0.1', **kwargs):
        """一键闪出平台"""
        balance = await self.get_user_balance(player.user_id)
        return await self.transfer(player,
                                   platform=platform,
                                   amount=balance['available_balance'],
                                   direction='OUT',
                                   client_ip=client_ip,
                                   **kwargs)

    @protect_transfer(user_or_player='user')
    async def transfer_allin(self, *, user: User, client_ip='127.0.0.1', **kwargs) -> typing.List[GameTransfer]:
        if await redis.set(f'lock:transfer:allin:{user.user_id}', value=1, exist='SET_IF_NOT_EXIST', expire=10):
            players = await self.get_players(user_id=user.user_id)
            tasks = [
                self._transfer_in(player=p, platform=p.platform, client_ip=client_ip, **kwargs)
                for p in players
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            def _(t):
                if isinstance(t, Exception):
                    return {'status': 'error', 'message': str(t)}
                elif isinstance(t, GameTransfer):
                    return {'status': t.status}
                return {'status': 'unknown'}

            data = [
                {'platform': player.platform, 'transfer': _(results[i])}
                for i, player in enumerate(players)
            ]
            logger.info('transfer.allin', tasks=len(tasks), user=user.user_id, data=data)
            await redis.delete(f'lock:transfer:allin:{user.user_id}')
            return data
        raise RateLimitExceeded

    async def transfer(self,
                       player: Player,
                       platform: str,
                       amount: Decimal,
                       direction: str,
                       client_ip="127.0.0.1",
                       raise_on_failed=True,
                       **kwargs) -> GameTransfer:
        """

        - 转入 IN: 从第三方将余额转入平台钱包
            - 发起转账API调用, 第三方扣款
            - 给平台会员加钱
        - 转出 OUT: 从平台钱包将余额转出至第三方
            - 平台预扣款
            - 发起转账API调用，转账给第三方
            - 二次确认转账成功

        注意事项：
            - 如果转账API返回平台余额以及平台订单号，需要更新到 GameTransfer 上, 以保证双方事务一致性

        @param player: 玩家对象
        @param platform: 平台
        @param amount: 金额
        @param direction:  转账方向
        @param client_ip: 客户端IP
        @param raise_on_failed: 失败的游戏转账订单，是否需要抛 exception
        @param kwargs:
        @return:
        """

        if player.is_guest:
            raise exceptions.DemoNotSupported("试玩账号不支持转账")

        s = self.get_service(platform)
        amount = s.format_currency(amount)
        if amount <= 0:
            raise exceptions.InSufficientMoney(f"中心钱包余额为：{amount}")
        transfer = GameTransfer(platform=s.platform,
                                username=player.username,
                                direction=direction,
                                order_no=s.new_billno(player=player),
                                client_ip=client_ip,
                                amount=amount,
                                user_id=player.user_id,
                                real_name=player.real_name,
                                **kwargs)
        fsm = self.get_fsm(player, s, transfer)
        fsm.initial(fsm.states.PENDING)
        try:
            await shutdown_waits_for(fsm.start())
        except asyncio.CancelledError:
            logger.warn('fsm.cancelled',
                        platform=transfer.platform,
                        order_no=transfer.order_no,
                        status=transfer.status,
                        direction=transfer.direction,
                        username=transfer.username,
                        user_id=transfer.user_id,
                        amount=transfer.amount)
        self.on_transfer_completed(transfer=transfer,
                                   player=player,
                                   raise_on_failed=raise_on_failed,
                                   error=fsm.error)
        return transfer

    def on_transfer_completed(self, transfer, player, raise_on_failed=True, error: Exception = None):
        """
        转账订单完成后，后续处理
        @param transfer:
        @param player:
        @param raise_on_failed:
        @param error:
        @return:
        """
        self.post_transfer(transfer=transfer, player=player)

        # on transfer fail
        if transfer.status == 'failed':
            self.on_transfer_failed(transfer=transfer, raise_on_failed=raise_on_failed, error=error)

    def on_transfer_failed(self, transfer, raise_on_failed=True, error=None):
        """
        转账订单失败后的处理
        @param transfer:
        @param raise_on_failed:
        @param error:
        @return:
        """
        if raise_on_failed:
            error = error or exceptions.GameTransferFailed(payload={
                "failure_code": transfer.failure_code, "failure_msg": transfer.failure_msg})
            raise error

    def post_transfer(self, transfer: GameTransfer, player: Player):
        """
        后置游戏转账处理
          - 后台刷新游戏平台余额
          - TODO: 记录活跃玩家
        """
        s = self.get_service(player.platform)
        delay = 0
        if s.LAUNCH_CONTAIN_TRANSFER:
            delay = 1
        self.update_wallet(player, delay=delay)

    def get_fsm(self, player, service, transfer: GameTransfer, **kwargs):
        if transfer.direction == 'IN':
            return GameTransferIn(player, service, transfer, **kwargs)
        return GameTransferOut(player, service, transfer, **kwargs)

    async def query_transfer(self, player: Player, transfer: GameTransfer, update_state=True):
        """
        查询游戏转账订单
        @param player:
        @param transfer:
        @param update_state:  如果订单结果有差异，是否自动更新订单状态
        @return:
        """
        s = self.get_service(transfer.platform)
        data = await s.query_transfer(transfer, player=player)
        result = s.parse_query_transfer(data)

        # states changed
        if update_state and result.status != transfer.status:
            fsm = self.get_fsm(player, s, transfer, result=result)
            state = fsm.states.SUCCEEDED if result.status == 'succeeded' else fsm.states.FAILED
            fsm.initial(state)
            await fsm.start()
        return result

    async def fetch_bets(self, platform: str, start: datetime, end: datetime, **kwargs):
        s = self.get_service(platform)
        print(f'fetch bets time: {start} ~ {end}')
        async for pagination in s.fetch_bets(start, end, **kwargs):
            print(pagination.result)

    def _get_collection_key_field(self, player):
        return 'game_collections', f'user:{player.user_id}'

    def _get_collection_game_key(self, game, game_id):
        return f'{game}:{game_id}'

    async def create_collection(self, player, platform, game, game_id):
        game_collections = await redis.hget(*self._get_collection_key_field(player))
        game_key = self._get_collection_game_key(game, game_id)
        if game_collections:
            game_collections = json_loads(game_collections)
            game_collections.setdefault(platform, {})
            game_collections[platform].update({game_key: 1})
            value = json_dumps(game_collections)
        else:
            value = json_dumps({platform: {game_key: 1}})
        await redis.hset(*self._get_collection_key_field(player), value)

    async def remove_collection(self, player, platform, game, game_id=0):
        game_collections = await redis.hget(*self._get_collection_key_field(player))
        game_key = self._get_collection_game_key(game, game_id)
        if game_collections:
            game_collections = json_loads(game_collections)
            if platform not in game_collections:
                raise exceptions.ValidationError(f"platform: {platform} 不存在收藏中")

            pop_value = game_collections[platform].pop(game_key, None)
            if pop_value == None:
                raise exceptions.ValidationError(f"game或game_id不存在收藏中")

            if game_collections[platform] == {}:
                game_collections.pop(platform, None)
            await redis.hset(*self._get_collection_key_field(player), json_dumps(game_collections))
            return
        raise exceptions.ValidationError(f"user: {player.username}還没有游戏收藏")

    async def get_collections(self, player):
        result = []
        game_collections = await redis.hget(*self._get_collection_key_field(player))
        if game_collections:
            game_collections = json_loads(game_collections)
            for platform, games in game_collections.items():
                for game_key in games.keys():
                    game, game_id = game_key.split(':')
                    result.append({
                        'platform': platform, 'game': game, 'game_id': game_id})
        return result


game_service = GameService()


async def init(app, loop):
    game_service.init_app(app=app, loop=loop)
    await game_service.state.init()


async def register(app, loop):
    """向网关注册服务"""
    pass


async def shutdown(app, loop):
    await game_service.close()
