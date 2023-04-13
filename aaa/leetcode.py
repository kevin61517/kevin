import json

def max_profit(prices):
    buy = None  # 買入價格
    profit = None  # 當前利潤
    for price in prices:
        if (buy is None) or (buy > price):
            buy = price
            continue

        tmp_profit = price - buy
        if (profit is None) or (tmp_profit > profit):
            profit = tmp_profit
    return profit or 0


def rd(nums) -> int:
    if len(nums) == 0:
        return 0
    i = 0
    for j in range(1, len(nums)):
        print('j===>', j)
        print('nums[j]==>', nums[j], 'nums[i]==>', nums[i])
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]
    print(nums)
    return i + 1


# def num2rom(num):
#     roms = {
#         1: 'I', 5: 'V',
#         10: 'X', 50: 'L',
#         100: 'C', 500: 'D', 1000: 'M',
#     }
#     divs = {
#         1: 1, 2: 10, 3: 100, 4: 1000
#     }
#     result = roms.get(num, '')
#     if result:
#         return result
#     str_n = f'{num}'
#     digits = len(str_n)
#     while digits:
#         number = int(str_n[-digits])
#         div = divs[digits]
#         rem = number % 5
#         if rem in [4, 1]:
#             if number > 5:
#                 print('===')
#                 left = roms[div]
#                 right = roms[divs[digits+1]]
#             else:
#                 left = roms[div]
#                 right = roms.get(5*div, roms.get(number))
#             rom = left + right if number > 1 else left
#         elif number == 5:
#             rom = roms[number * divs[digits]]
#         else:
#             if number <= 3:
#                 rom = ''.join([roms[div] for _ in range(number)])
#             else:
#                 rom = roms[div*5] + (number % 5) * roms[div]
#         result += rom
#         digits -= 1
#     return result


def num2rom_(num):
    roms = {
        1: 'I', 5: 'V',
        10: 'X', 50: 'L',
        100: 'C', 500: 'D', 1000: 'M',
    }
    divs = {
        1: 1, 2: 10, 3: 100, 4: 1000
    }
    result = roms.get(num, '')
    if result:
        return result
    str_n = f'{num}'
    for digit in range(len(str_n), 0, -1):
        number = int(str_n[-digit])
        div = divs[digit]
        if number == 5:
            result += roms[number * div]
        else:
            left = '' if number < 5 else f'{roms.get(5*div, roms[div])}'  # case div == 1000
            right = ''.join([roms[div] for _ in range(number % 5)])
            if len(right) > 3:
                left = roms[div]
                right = roms[5*div] if number < 5 else roms.get(divs.get(digit+1, divs[digit]))  # VIIII -> IX
            result += (left + right)
    return result


if __name__ == '__main__':
    ps = [7, 1, 5, 3, 6, 4]
    r = max_profit(ps)
    print(num2rom_(1))
    print('a.b.c.d'.rsplit('.', 1))
    path = 'slot-images/BBIN/zhenrenyule/zhenrenyule.jpg'
    block = path.split('/')
    print(block)
    img = block.pop(-1)
    img_name = ''.join(img.rsplit('.', 1))
    block.append(img_name)
    print('/'.join(block))
    ps = [' AGIN', ' AGIN', ' HUNTER', 'AG', 'AG', 'AG', 'AGIN', 'BBIN', 'BBIN', 'BBIN', 'BBINSlot', 'BBNSlot', 'BG', 'BG', 'BGSlot', 'CQ', 'GMMGSlot', 'GMPT', 'HG', 'IGSlot', 'JDB', 'KY', 'MG', 'MGSlot', 'OG', 'PG', 'SABAH', 'SBTA', 'TTG', 'VR', 'XBBSlot', 'XIN', 'XIN', 'XIN', 'YOPLAY']
    r = list(set([p.replace(' ', '') for p in ps]))
    print(r)
    a = 'slot-images/GMMGSlot/breakawayshootout.png'
    domain = """aa.com,bb.com,cc.com,dd.com,    ee.com"""
    history_data = '1:2'.split(':')
    _3 = 'haha'
    if len(history_data) == 3:
        _1, _2, _3 = history_data
    else:
        _1, _2 = history_data
    print(_1, _2, _3)
    for d in domain.replace(' ', '').split(','):
        print(json.dumps(d))


    def add_val_to_list(val, lst=[]):
        lst.append(val)
        return lst

    list1 = add_val_to_list(321)
    print(list1)

    list2 = add_val_to_list(123, [])
    print(list2)

    list3 = add_val_to_list('a')
    print(list3)
