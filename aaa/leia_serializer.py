from datetime import datetime, timedelta


class Serializer:
    __hidden__ = []

    def to_json(self):
        json_data = {}
        for attr_name in self.__dir__():
            if not attr_name.startswith('__') and attr_name not in self.__hidden__:
                attr = getattr(self, attr_name)
                if not callable(attr):
                    json_data[attr_name] = attr
        return json_data


class A(Serializer):
    def __init__(self):
        self.name = 'leia'
        self.number = 111
        self.school = 'NSYSU'


def red_envelope(times):
    """2022-10-01 ~ 2022-10-07紅包活動"""
    _0 = [0 for _ in range(50)]
    _1 = [1 for _ in range(20)]
    _5 = [5 for _ in range(15)]
    _8 = [8 for _ in range(10)]
    _18 = [18 for _ in range(3)]
    _38 = [38 for _ in range(2)]
    reward_map = _0 + _1 + _5 + _8 + _18 + _38
    reward_amount = 0
    for _ in range(times):
        index = random.randint(0, 99)
        reward_amount += reward_map[index]
    return reward_amount


if __name__ == '__main__':
    import random
    lst = []
    for i in range(10000):
        amount = random.choices(['0', '1', '5', '8', '18', '38'], weights=[50, 20, 15, 10, 3, 2])[0]
        if amount == '0':
            lst.append(amount)
    print(len(lst))
    dt = datetime.now() + timedelta(days=1)
    
    print(dt.date())


# d = {
#     "level_1_detail": {
#         "AGIN": {
#             "net_amount": "12233.60",
#             "valid_amount": "735305.20",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "611.68"
#         },
#         "KY": {
#             "net_amount": "-2188.48",
#             "valid_amount": "2520.00",
#             "rental_fee_rate": "0.05", "rental_fee_platform": 0
#         },
#         "LH": {
#             "net_amount": "1964.80",
#             "valid_amount": "5824.0000",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "98.24"
#         },
#         "LY": {
#             "net_amount": "-600.60",
#             "valid_amount": "3308.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         }
#     },
#     "level_2_detail": {
#         "AGIN": {
#             "net_amount": "12233.60",
#             "valid_amount": "735305.20",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "611.68"
#         },
#         "KY": {
#             "net_amount": "-2188.48",
#             "valid_amount": "2520.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         },
#         "LH": {
#             "net_amount": "1964.80",
#             "valid_amount": "5824.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "98.24"
#         },
#         "LY": {
#             "net_amount": "-600.60",
#             "valid_amount": "3308.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         }
#     },
#     "level_3_detail": {
#         "AGIN": {
#             "net_amount": "12233.60",
#             "valid_amount": "735305.20",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "611.68"
#         },
#         "KY": {
#             "net_amount": "-2188.48",
#             "valid_amount": "2520.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         },
#         "LH": {
#             "net_amount": "1964.80",
#             "valid_amount": "5824.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "98.24"
#         },
#         "LY": {
#             "net_amount": "-600.60",
#             "valid_amount": "3308.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         }
#     },
#     "detail_total": {
#         "AGIN": {
#             "net_amount": "12233.60",
#             "valid_amount": "735305.20",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "611.68"
#         },
#         "KY": {
#             "net_amount": "-2188.48",
#             "valid_amount": "2520.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         },
#         "LH": {
#             "net_amount": "1964.80",
#             "valid_amount": "5824.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": "98.24"
#         },
#         "LY": {
#             "net_amount": "-600.60",
#             "valid_amount": "3308.00",
#             "rental_fee_rate": "0.05",
#             "rental_fee_platform": 0
#         }
#     }
# }

"""
mysql> select * from userbet_platform_type_daily where user_id=2332;
+---------------------+---------------------+--------------+----------+----------+--------------+------------+------------+----------------+-----------------+------------+------------+----+---------+----------+---------+-------------+------+---------+-----------+-------------+---------+-----------+------------+-------------+-------------+
| created             | updated             | player_name  | username | currency | valid_amount | bet_amount | net_amount | revenue_amount | user_commission | commission | total_bets | id | user_id | platform | type    | amount_paid | paid | paid_at | total_fee | valid_ratio | status  | client_ip | op_user_id | op_username | device_type |
+---------------------+---------------------+--------------+----------+----------+--------------+------------+------------+----------------+-----------------+------------+------------+----+---------+----------+---------+-------------+------+---------+-----------+-------------+---------+-----------+------------+-------------+-------------+
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    6270.0000 |  6270.0000 | -1860.0000 |      1860.0000 |          0.0000 |     0.0000 |         27 |  3 |    2332 | BG       | esport  |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    8193.0000 |  8193.0000 |  -461.0000 |       461.0000 |          0.0000 |     0.0000 |         28 |  6 |    2332 | BG       | fish    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    8357.0000 |  8357.0000 |  2775.0000 |     -2775.0000 |          0.0000 |     0.0000 |         32 |  1 |    2332 | BG       | live    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    4666.0000 |  4666.0000 |  1952.0000 |     -1952.0000 |          0.0000 |     0.0000 |         24 |  8 |    2332 | BG       | lottery |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    5433.0000 |  5433.0000 |  1011.0000 |     -1011.0000 |          0.0000 |     0.0000 |         26 | 11 |    2332 | BG       | poker   |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    8866.0000 |  8866.0000 | -1792.0000 |      1792.0000 |          0.0000 |     0.0000 |         33 | 14 |    2332 | BG       | slot    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-08-29 16:00:00 | 2022-08-30 15:50:12 | testxutest15 | xutest15 | CNY      |    7630.0000 |  7630.0000 | -1678.0000 |      1678.0000 |          0.0000 |     0.0000 |         30 |  7 |    2332 | BG       | sport   |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
+---------------------+---------------------+--------------+----------+----------+--------------+------------+------------+----------------+-----------------+------------+------------+----+---------+----------+---------+-------------+------+---------+-----------+-------------+---------+-----------+------------+-------------+-------------+
7 rows in set (0.00 sec)
"""

"""
mysql> select * from userbet_platform_type_daily where user_id=2352;
+---------------------+---------------------+-----------------+-------------+----------+--------------+------------+------------+----------------+-----------------+------------+------------+------+---------+----------+---------+-------------+------+---------+-----------+-------------+---------+-----------+------------+-------------+-------------+
| created             | updated             | player_name     | username    | currency | valid_amount | bet_amount | net_amount | revenue_amount | user_commission | commission | total_bets | id   | user_id | platform | type    | amount_paid | paid | paid_at | total_fee | valid_ratio | status  | client_ip | op_user_id | op_username | device_type |
+---------------------+---------------------+-----------------+-------------+----------+--------------+------------+------------+----------------+-----------------+------------+------------+------+---------+----------+---------+-------------+------+---------+-----------+-------------+---------+-----------+------------+-------------+-------------+
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |    2791.0000 |  2791.0000 | -1125.0000 |      1125.0000 |          0.0000 |     0.0000 |          8 | 1343 |    2352 | BG       | esport  |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |    1281.0000 |  1281.0000 |   663.0000 |      -663.0000 |          0.0000 |     0.0000 |          6 | 1339 |    2352 | BG       | fish    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |    1539.0000 |  1539.0000 | -1109.0000 |      1109.0000 |          0.0000 |     0.0000 |          6 | 1345 |    2352 | BG       | live    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |     961.0000 |   961.0000 |  -457.0000 |       457.0000 |          0.0000 |     0.0000 |          6 | 1338 |    2352 | BG       | lottery |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |    3415.0000 |  3415.0000 |  -391.0000 |       391.0000 |          0.0000 |     0.0000 |         13 | 1351 |    2352 | BG       | poker   |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |    1106.0000 |  1106.0000 |   726.0000 |      -726.0000 |          0.0000 |     0.0000 |          4 | 1325 |    2352 | BG       | slot    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-09-05 16:00:00 | 2022-09-06 15:50:19 | testceshidaili5 | ceshidaili5 | CNY      |    2212.0000 |  2212.0000 |  1732.0000 |     -1732.0000 |          0.0000 |     0.0000 |          7 | 1327 |    2352 | BG       | sport   |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |    2153.0000 |  2153.0000 | -2153.0000 |      2153.0000 |          0.0000 |     0.0000 |         10 | 1583 |    2352 | BG       | esport  |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |    2265.0000 |  2265.0000 | -2265.0000 |      2265.0000 |          0.0000 |     0.0000 |          9 | 1587 |    2352 | BG       | fish    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |    1898.0000 |  1898.0000 | -1898.0000 |      1898.0000 |          0.0000 |     0.0000 |          8 | 1580 |    2352 | BG       | live    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |     681.0000 |   681.0000 |  -681.0000 |       681.0000 |          0.0000 |     0.0000 |          3 | 1590 |    2352 | BG       | lottery |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | H5          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |    1000.0000 |  1000.0000 | -1000.0000 |      1000.0000 |          0.0000 |     0.0000 |          5 | 1592 |    2352 | BG       | poker   |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |    1944.0000 |  1944.0000 | -1944.0000 |      1944.0000 |          0.0000 |     0.0000 |          8 | 1577 |    2352 | BG       | slot    |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
| 2022-09-06 16:00:00 | 2022-09-07 15:50:15 | testceshidaili5 | ceshidaili5 | CNY      |    1509.0000 |  1509.0000 | -1509.0000 |      1509.0000 |          0.0000 |     0.0000 |          7 | 1578 |    2352 | BG       | sport   |        0.00 |    0 | NULL    |      0.00 |      0.0000 | pending | 127.0.0.1 |       NULL | NULL        | PC          |
+---------------------+---------------------+-----------------+-------------+----------+--------------+------------+------------+----------------+-----------------+------------+------------+------+---------+----------+---------+-------------+------+---------+-----------+-------------+---------+-----------+------------+-------------+-------------+
14 rows in set (0.00 sec)
"""