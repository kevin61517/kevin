"""
OB 真人
✔ 创建玩家
✔  游戏启动
✔  游戏转入
✔  游戏转出
✔  一键闪入
✔  一键闪出
✔  查询余额
✔ 查询转账
✔ 注单拉取
三方注單返回格式：
{
    'uuid': '0bb39695-28de-42d2-9287-fb051544ce0c',
    'timestamp': '2022-12-05T02:56:30Z',
    'data': [
        {
            'date': '2022-12-02',
            'games': [
                {
                    'settledAt': '2022-12-02T02:19:28.014Z',
                    'payout': '20.00000',
                    'dealer': {'uid': 'tts0r7h_________', 'name': 'ROB_269'},
                    'result': {
                        'dealtToPlayer': ['QH', '6C', '4D'],
                        'dealerHand': {'score': 17, 'cards': ['7S', 'QS']},
                        'wonSideBets': []
                    },
                    'participants': [
                        {
                            'casinoId': '1i3s03x5brtt4gli',
                            'playerId': '39',
                            'screenName': 'ceshievo',
                            'playerGameId': '172cd86a01bead8adf4c0096-qtf45fmk62mqbgo4',
                            'sessionId': 'qtf45fmk62mqbgo4qtij5b35uqkaahxe249cdfb2',
                            'casinoSessionId': '',
                            'currency': 'CNY',
                            'bets': [
                            {
                                'code': 'FBBJ_AnyPair',
                                'stake': 10,
                                'payout': 0,
                                'placedOn': '2022-12-02T02:18:50.716Z',
                                'description': 'Any Pair',
                                'transactionId': '669649203066825087'
                            },
                            {
                                'code': 'FBBJ_Main',
                                'stake': 10,
                                'payout': 20,
                                'placedOn': '2022-12-02T02:18:50.716Z',
                                'description': 'Main Bet',
                                'transactionId': '669649203066825087'
                            }
                        ],
                            'configOverlays': [],
                            'playMode': 'RealMoney',
                            'channel': 'desktop',
                            'os': 'macOS',
                            'device': 'Desktop',
                            'skinId': '1',
                            'brandId': '1',
                            'hands': {
                                'hand1': {
                                    'cards': ['QH', '6C', '4D'], 'decisions': [{'type': 'Hit'}, {'type': 'Stand'}],
                                    'outcome': 'Win', 'score': 20, 'position': 'Main'
                                }
                            }
                        }
                    ],
                    'id': '172cd86a01bead8adf4c0096',
                    'gameType': 'freebet',
                    'status': 'Resolved',
                    'startedAt': '2022-12-02T02:18:31.654Z',
                    'currency': 'CNY',
                    'wager': '20.00000',
                    'table': {'id': 'FreeBet000000001','name': 'Free Bet Blackjack'}
                },
                {...},
                {...}
            ]
        }
    ]
}
"""
import asyncio
import uuid
import hashlib
import typing
import time
import urllib.parse
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
import base64

import attr
import pytz
import tenacity
from delorean import Delorean

from rpc.logger import get_logger
from rpc.client import HTTPResponse
from rpc.server.helpers import json_dumps, json_loads
from rpc.server.services.game.interface import PlatformService
from rpc.server.services.game.token import TokenService
from rpc.server.objects import User, Player, Game, Launch, GameTransfer, GameTransferResult, Pagination, Query
from rpc.server.services.game.fsm import States
from rpc.utils import to_decimal, parse_dt
from spinach import exceptions
from spinach.constants import ST_WIN, ST_LOSE, ST_DRAW, ST_RESET, ST_SYSTEM_CANCELED, LOCAL_TZ

logger = get_logger(__name__)

ERRORS = {
    '601': '参数异常',
    '629': '访问频繁',
    '700': '系统错误',
    '600': '缺少参数'
}

retry = tenacity.retry(reraise=True,
                       retry=tenacity.retry_if_exception_type(
                           exception_types=(
                               exceptions.NetworkError,  # 网络错误
                               exceptions.RetryError,  # 重试错误
                           )
                       ),
                       wait=tenacity.wait_fixed(4),
                       stop=tenacity.stop_after_attempt(10))


@attr.s(slots=True, kw_only=True)
class Conf:
    # API
    api: str = attr.ib(default="https://staging.evolution.asia-live.com")  # 遊戲api
    bet_api = attr.ib(default="https://stage-admin.asia-live.com")  # 注單api
    # 配置
    mch_id: str = attr.ib(default='433004STA')
    casino_key = attr.ib(default="1i3s03x5brtt4gli")  # key
    api_token = attr.ib(default="9c1e9d7b8853f91174fc3e3dddbee4d8")  # api token


class EVO(Conf, PlatformService):
    BET_TIMEDELTA = timedelta(minutes=30)
    BET_TIMEZONE = 'Asia/Shanghai'
    BET_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    NAME_SALT_LENGTH = 2
    PAGE_SIZE = 100000
    _aliases = ['EVOLIVE']
    FAIL_STATUS = {
        'INVALID_PARAMETER': '10002',
        'TEMPORARY_ERROR': '1001',
        'INVALID_TOKEN_ID': '10003',
        'INVALID_SID': '10003',
        'UNKNOWN_ERROR': '1049',
        'BET_DOES_NOT_EXIST': '10005',
        'INSUFFICIENT_FUNDS': '10008',
    }
    API_ACTIONS = {
        'IN': 'EDB',
        'OUT': 'ECR',
        'QUERY_TRANSFER': 'TRI',
        'QUERY_BALANCE': 'RWA',
    }
    #  (正常返回, 錯誤返回)
    QUERY_STATUS_KEYS = {
        'TRI': ('transaction', 'error'),
        'RWA': ('userbalance', 'error'),
        'EDB': ('transfer', 'transfer'),
        'ECR': ('transfer', 'transfer')
    }

    @staticmethod
    def stamp_time() -> str:
        return f'{int(time.time())}'

    def configure_cipher(self):
        """配置Cipher初始化参数"""
        pass

    def url_for(self, path, is_history=False, **kwargs) -> str:
        """生成完整请求url"""
        if is_history:
            return f'{self.bet_api}{path}'
        return f'{self.api}{path}'

    def gen_headers(self):
        source = f'{self.casino_key}:{self.api_token}'
        pw = base64.b64encode(source.encode()).decode()
        return {'Authorization': f'Basic {pw}'}

    def new_player_name(self, user: User) -> str:
        name = super(EVO, self).new_player_name(user)
        return f'{self.mch_id}{name}'

    async def _create_player(self, player: Player, client_ip="127.0.0.1") -> dict:
        """創建玩家"""
        url = self.url_for(f'/ua/v1/{self.casino_key}/{self.api_token}')
        name = player.real_name or player.player_name
        player_config = {
            'id': player.player_name,
            'update': True,
            'firstName': name,
            'lastName': name,
            'language': 'CN',
            'country': 'CN',
            'currency': 'CNY',
            'session': {'id': '', 'ip': client_ip if client_ip else "127.0.0.1"}
        }
        payload = {
            'uuid': str(uuid.uuid4()),
            'player': player_config,
            'config': {'game': {'category': 'all_games'}},
            'channel': {'wrapped': True},
        }
        result = await self._post(url, json=payload, timeout=30)
        return result

    async def create_player(self, user: User, client_ip="127.0.0.1", **kwargs) -> Player:
        player = self.new_player(user)
        await self._create_player(player, client_ip=client_ip)
        return player

    async def launch(self, player: Player, game: Game, client_ip="18.166.200.86", **kwargs) -> Launch:
        """
        1.發請求
        2.取得驗證, 登入url
        3.進入遊戲
        game.game = all_games -> 返回遊戲大廳地址
        """
        url = self.url_for(f'/ua/v1/{self.casino_key}/{self.api_token}')
        name = player.real_name or player.player_name
        player_config = {
            'id': player.player_name,
            'update': True,
            'firstName': name,
            'lastName': name,
            'country': 'CN',
            'language': 'CN',
            'currency': 'CNY',
            'session': {'id': '', 'ip': client_ip if client_ip else "18.166.200.86"}
        }
        payload = {
            'uuid': str(uuid.uuid4()),
            'player': player_config,
            'config': {'game': {'category': 'all_games'}},
            'channel': {'wrapped': True},
        }
        result = await self._post(url, json=payload)
        return Launch(url=result.get('entry'), method='get', redirect=True)

    def verify_payload(self, data: dict) -> dict:
        """
        校验第三方API返回结果
        結構基本上是
        {
            "code": 狀態碼(string)，成功為200，錯誤的部分在代碼中有定義ERROR變數,
            "message": 訊息(string),
            "request": 原入參資料(dict),
            "data": 返回數據(dict)
        }
        """
        if not data.get('entry'):
            error = data.get('userbalance')
            failure_msg = error.get('errormsg')
            raise exceptions.ChannelResponseCodeFail(
                failure_msg,
                payload={
                    'failure_msg': failure_msg,
                    'failure_code': failure_msg
                }
            )
        return data

    @staticmethod
    def verify_query_payload(data: dict, query_status_key_tuple: tuple) -> dict:
        """"""
        if not query_status_key_tuple:
            # 拉注單
            return data
        # 正常返回
        r: dict = data.get(query_status_key_tuple[0])
        if not r:
            # 錯誤返回
            r: dict = data.get(query_status_key_tuple[1])
        if r.get('result') != 'Y':
            failure_code = r.get('result')  # Y, N
            failure_msg = r.get('errormsg')
            raise exceptions.ChannelResponseCodeFail(
                failure_msg,
                payload={
                    'failure_msg': failure_msg,
                    'failure_code': failure_code
                }
            )
        return data

    def verify_resp_status(self, resp: HTTPResponse):
        """
        检查HTTP状态码
        一些平台会根据HTTP状态码做一些特殊判定，比如繁忙，可重新覆盖重写该方法达到自动重试机制
        """
        code = json_loads(resp.content.decode('utf8')).get('code', 200)
        if code == 629:  # 查询请求过于频繁
            raise exceptions.RetryError(wait=10)
        super(EVO, self).verify_resp_status(resp)

    @retry
    async def _request(self, url,
                       method='GET',
                       params=None, data=None, json=None, headers=None, cookies=None,
                       **kwargs) -> \
            typing.Union[list, dict]:

        _stats = self._request.retry.statistics
        logger.debug(f"request", platform=self.platform, method=method, url=url,
                     params=params, data=data, json=json, headers=headers, cookies=cookies,
                     kwargs=kwargs, retry_stats=_stats)
        resp = await self._client.fetch(url=url,
                                        method=method,
                                        params=params, data=data, json=json, headers=headers, cookies=cookies,
                                        **kwargs)
        self.verify_resp_status(resp)
        result = self.parse_resp(resp)
        if method == 'GET':
            query_status_key_tuple = self.QUERY_STATUS_KEYS.get(params.get('cCode'))
            return self.verify_query_payload(result, query_status_key_tuple)
        return self.verify_payload(result)

    async def has_player(self, player: Player) -> bool:
        pass

    def has_demo(self, game: Game = None) -> bool:
        """是否支持试玩"""
        return False

    async def query_balance(self, player: Player) -> Decimal:
        """查询平台余额"""
        url = self.url_for(f'/api/ecashier')
        payload = {
            'cCode': 'RWA',
            'ecID': self.casino_key,
            'euID': player.player_name,
            'output': '0'
        }
        result = await self._get(url=url, params=payload, timeout=30)
        return to_decimal(result['userbalance']['tbalance'])

    async def kick(self, player: Player) -> bool:
        """未提供"""
        pass

    # TODO
    async def query_credit(self, player: Player) -> Decimal:
        """查询商户额度"""

    def prepare_transfer(self, player: Player, transfer: GameTransfer, **kwargs) -> typing.Union[dict, str]:
        """
        第三方文件說的
        EDB: Game -> Spinach
        ECR: Spinach -> Game
        TRI: query_transfer
        """
        actions = {
            'IN': 'EDB',
            'OUT': 'ECR'
        }
        action = actions.get(transfer.direction, 'TRI')
        return {
            'cCode': action,
            'ecID': self.casino_key,
            'euID': player.player_name,
            'eTransID': transfer.order_no,
            'amount': f'{transfer.amount}',
            'createuser': 'Y',
            'output': '0'
        }

    @staticmethod
    def format_back_url(back_url: str):
        if not back_url.startswith('http'):
            return f'https://{back_url}'
        return back_url

    async def login(self, player: Player, url: dict = None):
        """"""
        pass

    async def logout(self, player: Player):
        pass

    async def online(self, player: Player) -> bool:
        pass

    async def transfer(self, transfer: GameTransfer) -> dict:
        """平台转账"""
        data = dict(transfer.extra['params'])
        url = self.url_for('/api/ecashier')
        result = await self._get(url, params=data, timeout=30)
        return result

    async def transfer_ack(self, transfer: GameTransfer, error: typing.Union[exceptions.GameTransferAckError,
                                                                             exceptions.GameTransferFailed,
                                                                             exceptions.RetryError]) -> GameTransferResult:
        pass

    def parse_transfer(self, transfer: GameTransfer, result: dict) -> GameTransferResult:
        """
        处理转账返回的结果， 如果转账状态码失败，则需要抛出异常 GameTransferFailed 的异常
        部分第三方会回传第三方订单号，以及账户资金余额，可以用于更新 GameTransfer 相关字段
        @param transfer:
        @param result:
        @return:
        """
        code = result.get('code')
        status = States.SUCCEEDED.value
        succeeded = 0
        failure_code = None
        failure_msg = None
        if code != succeeded:
            status = States.FAILED.value
            failure_code = code
            failure_msg = result.get('msg', f'未知错误码:{status}')
        return GameTransferResult(
            status=status,
            succeeded=succeeded,
            failure_code=failure_code,
            failure_msg=failure_msg,
            amount=transfer.amount,
            result=result
        )

    async def query_transfer(self, transfer: GameTransfer, player=None) -> typing.Union[dict, list]:
        """
        需要實測取得轉帳
        """
        data = dict(transfer.extra)
        data.setdefault('cCode', 'TRI')
        url = self.url_for('/api/ecashier')
        result = await self._get(url, params=data.get('params', {}), timeout=30)
        return result

    def parse_query_transfer(self, result: typing.Union[dict, list]) -> GameTransferResult:
        """
        处理查询游戏转账返回的结果
        """
        r = result.get('transaction', {})
        code = r.get('result')
        if code == 'Y':
            return GameTransferResult(
                succeeded=True,
                status='succeeded',
                result=result
            )

        return GameTransferResult(
            succeeded=False,
            status='failed',
            result=result,
            failure_code=code,
            failure_msg=r.get('errormsg', f'未知错误码:failed')
        )

    def format_time(self, dt: datetime) -> str:
        """
        @param dt: 带时区的时间对象
        @return:
        """
        r = dt.astimezone(pytz.timezone(self.BET_TIMEZONE)).strftime(self.BET_TIME_FORMAT)
        return f'{r[:-3]}Z'

    async def fetch_bets(self,
                         start: datetime,
                         end: datetime,
                         gap: timedelta = timedelta(minutes=5),
                         **kwargs) -> typing.AsyncIterator[Pagination]:
        """
        拉取一个时间范围内的所有注单，返回一个结果列表

        因注单平台时间范围取值会有所限制，在查询一个时间范围内，会将起始时间 start ~ 结束时间 end 做一个
        切分 N 个注单平台支持的 t1 ~ t2 时间范围
        每 t1 ~ t2 时间范围内，会返回 M 个 Pagination 分页对象

        start ~ end 时间范围 -> 切分 N 个 t1 ~ t2
        每 t1 ~ t2 时间范围内返回 M 个 Pagination 分页对象

        Query(t1 ~ t2) => [Pagination(1)][Pagination(2][Pagination(3)]...[Pagination(M-1)][Pagination(M)]

        Pagination:
            - has_next bool: 是否还有下一页
            - next int: 下一页码

        delta:  每次注单时间查询最大时间范围，比如：一些平台单次查询注单只能限定30分钟,1小时内
        @param start:  带时区的时间对象
        @param end:  带时区的时间对象
        @param gap:  为保证获取时间范围内数据完整性，会将start，end的时间范围延长这个长度，通常我们取5分钟
        @param kwargs:  查询所需要的额外参数, 传递到下一层平台查询接口里
        @return: List
        """
        delta = self.BET_TIMEDELTA
        t1 = start - gap
        end = end - timedelta(seconds=30)
        t2 = min(t1 + delta, end)
        while t1 < end:
            has_next = True
            page = 1
            # 一个 query 查询对象下，会存在M个分页对象,读取直至最后一个分页对象
            while has_next:
                q = self.next_query(t1, t2, page=page, **kwargs)
                async for pagination in self.query_bets(q):
                    yield pagination
                    # 递增页数
                    page = pagination.next or page + 1
                    # 当前查询最末一个分页对象, 跳出循环
                    has_next = pagination.has_next

            t1 = t2
            t2 = min(t2 + delta, end)

    def next_query(self, start, end, page=1, **kwargs) -> Query:
        """查询注单参数对象"""
        return Query(
            start=start,
            end=end,
            page=page,
            params={
                'startDate': self.format_time(start),
                'endDate': self.format_time(end)
            }
        )

    async def query_bets(self, query: Query) -> typing.AsyncIterator[Pagination]:
        """
        回傳值:
        {
            'uuid': 'c2414ff7-2288-4fa2-8342-49eb53833668',
            'timestamp': '2022-12-01T17:42:10Z',
            'data': [
                {
                    'date': '2022-12-01',
                    'games': [
                        {
                            'settledAt': '2022-12-01T16:15:03.703Z',
                            'payout': '20.00000',
                            'dealer': {'uid': 'tts0rh__________', 'name': 'ROB_17'},
                            'result': {'outcomes': ['01']},
                            'participants': [
                                {
                                    'casinoId': '1i3s03x5brtt4gli',
                                    'playerId': '39',
                                    'screenName': 'ceshievo',
                                    'playerGameId': '172cb7725755b5ed6e2b51c9-qtf45fmk62mqbgo4',
                                    'sessionId': 'qtf45fmk62mqbgo4qthhk3vkssjqaagd4478a99b',
                                    'casinoSessionId': '',
                                    'currency': 'CNY',
                                    'bets': [
                                        {
                                            'code': 'MW_One',
                                            'stake': 10,
                                            'payout': 20,
                                            'placedOn': '2022-12-01T16:14:43.650Z',
                                            'description': '1',
                                            'transactionId': '669886641129088315'
                                        }
                                    ],
                                    'configOverlays': [],
                                    'playMode': 'RealMoney',
                                    'channel': 'desktop',
                                    'os': 'macOS',
                                    'device': 'Desktop',
                                    'skinId': '1',
                                    'brandId': '1',
                                    'maxMultiplier': 20000
                                }
                            ],
                            'id': '172cb7725755b5ed6e2b51c9',
                            'gameType': 'moneywheel',
                            'status': 'Resolved',
                            'startedAt': '2022-12-01T16:14:23.567Z',
                            'currency': 'CNY',
                            'wager': '10.00000',
                            'table': {
                                'id': 'MOWDream00000001',
                                'name': 'DNT Dream Catcher'
                            }
                        }, {...}, {...}
                    ]
                }
        wager: 該局總注額
        stake: 單筆注額(一局可能有很多筆)
        payout: 注額+輸贏
        輸贏: payout - wager(總額-注額)
        """
        params = query.params
        path = f'/api/gamehistory/v1/casino/games'
        url = self.url_for(path=path, is_history=True)
        headers = self.gen_headers()
        result = await self._get(url=url, params=params, headers=headers)
        yield self.paginate(result, query)

    def parse_bet_time(self, time_, timezone=None, str_format=None):
        """
        处理注单时间，转换为 UTC 时区时间, 方便入库
        @param time_:
        @param timezone:
        @param str_format:
        @return:
        """
        timezone = timezone or self.BET_TIMEZONE
        str_format = str_format or self.BET_TIME_FORMAT
        return parse_dt(time_[:-1], time_zone=timezone, str_format=str_format)

    def paginate(self, result: dict, query: Query = None, **kwargs) -> Pagination:
        """天數(三方拉取得注單title帶著日期) -> [{'date': '2022-12-02', 'games': [{...}, {...}]}]"""
        items = []
        for day in result['data']:
            games = day.get('games')
            items += [self.parse_bet(items) for items in games]
        return Pagination(result=result, total=len(items), has_next=False, next=None, items=items)

    def parse_bet(self, item) -> dict:
        """
        總額 = 下注金額 + 輸贏金額
        ST_WIN = 玩家贏
        ST_LOSE = 玩家輸
        """
        # 玩家輸贏(總額-注額)
        net_amount = Decimal(item.get('payout')) - Decimal(item.get('wager'))
        # 有效注額
        valid_amount = item.get('wager')
        # 平台輸贏
        revenue_amount = net_amount * -1
        # 下注前額度(三方未提供)
        start_balance = last_balance = 0
        # 遊戲名稱
        game_name = item.get('table').get('name')
        if net_amount > 0:
            status = ST_WIN
        elif net_amount < 0:
            status = ST_LOSE
        else:
            status = ST_DRAW

        bet_time = self.parse_bet_time(item.get('startedAt'))  # startedAt -> 開始時間
        record_time = self.parse_bet_time(item.get('settledAt'))  # settledAt -> 結算時間

        return {
            'platform': self.__class__.__name__,
            'player_name': item.get('participants')[0].get('playerId'),  # participants[0].get('playerId') -> 參與人員
            'bet_time': bet_time,  # v
            'report_time': record_time,  # 結算時間 v
            'payout_time': record_time,  # 結算時間 v
            'start_balance': f'{start_balance}',  # 下单前注单额度  x
            'status': status,  # 注单状态，輸、贏、平手 v if ,Trur  v ->
            'bill_no': item.get('id'),  # 注单单号 -> transactionId v
            'bet_amount': f'{valid_amount}',  # 下注金额 -> stake(單注)
            'valid_amount': f'{valid_amount}',  # 有效金额 -> wager(該場遊戲總注額)
            'net_amount': f"{net_amount}",  # 输赢额度  v ->
            'payout_amount': revenue_amount,  # 若无派彩金额则使用输赢额度  v
            'settled': True,  # 是否结算，第三方只返回以結算注單，參考query_bets的說明
            'game_code': game_name,  # 系统内的GameId
            'game_name': game_name,  # -> table: {'name': '...'}
            'device_type': 'PC',
            'data': item,
            'last_balance': last_balance,  # 三方未提供
            'revenue_amount': f"{revenue_amount}",  # Spinach輸贏 v
            'last_updated': record_time,  # 使用結算時間 v
            'type': item.get('gameType'),  # -> gameType
        }
