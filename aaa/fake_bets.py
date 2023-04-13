import argparse
import asyncio
import random
import pytz
from delorean import Delorean

# from rpc.constants import TENANT_ID
from rpc.server.db import mongo_manager
from rpc.server.db.mongo import mongo_service
from spinach.constants import ST_WIN, ST_LOSE, LOCAL_TZ
from spinach.helpers import new_order_no


async def main(reset=False, win_or_lose=0):
    from rpc.constants import TENANT_ID
    await mongo_manager.setup(None, None)
    try:
        if reset:
            await mongo_service.delete_many({'user_id_in': ['2592', '2593', '2594', 2592, 2593, 2594]})
        created = bet_time = payout_time = last_updated = Delorean(
            timezone=LOCAL_TZ).datetime.replace(microsecond=False).astimezone(pytz.UTC).isoformat()
        sample_document = {
            "game_code": "777",
            "currency": "CNY",
            "game_name": "FAKE GAME",
            "bet_content": "FAKE CONTENT",
            "settled": True,
            "data": {},
            "result": "",
            "created": created,
            "bet_time": bet_time,
            "payout_time": payout_time,
            "last_updated": last_updated,
            "report_time": bet_time,
        }
        fake_documents = []
        fp1 = {'player_uid': '2592', 'user_id': '2592', 'username': 'fp0001'}
        fp2 = {'player_uid': '2593', 'user_id': '2593', 'username': 'fp0002'}
        fp3 = {'player_uid': '2594', 'user_id': '2594', 'username': 'fp0003'}
        us = [fp1, fp2, fp3]
        quantity_of_bets = random.randint(50, 100)
        for count in range(quantity_of_bets):
            if not win_or_lose:
                win_or_lose = random.choice([1, -1])
            status = ST_WIN if win_or_lose == 1 else ST_LOSE
            start_balance = random.randint(1000, 2000)
            bet_amount = valid_amount = random.randint(1, 5000)
            platform = random.choice(['AG', 'BG', 'MG', 'BBN'])
            device_type = random.choice(['PC', 'H5'])
            game_type = random.choice(['slot', 'live'])
            user = random.choice(us)
            player_name = f'{TENANT_ID}{user["username"]}'
            net_amount = valid_amount * win_or_lose
            document = dict(
                platform=platform,
                bill_no=new_order_no()[1:-3],
                bet_amount=bet_amount,
                valid_amount=valid_amount,
                device_type=device_type,
                start_balance=start_balance,
                status=status,
                net_amount=net_amount,
                payout_amount=net_amount,
                revenue_amount=net_amount * -1,
                last_balance=start_balance + net_amount,
                type=game_type,
                jackpot_amount='0',
                jackpot_type=0,
                room=new_order_no()[1:-3],
                player_name=player_name,
                **sample_document,
                **user,
            )
            fake_documents.append(document)
        await mongo_service.insert_many(documents=fake_documents)

    finally:
        await mongo_manager.close(None, None)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', type=bool, default=False)
    parser.add_argument('--win_or_lose', type=int, default=0)
    args = parser.parse_args()

    loop.run_until_complete(main(args.reset, args.win_or_lose))
