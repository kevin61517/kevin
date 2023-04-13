import time
import sys

nums = [n for _ in range(20) for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)]
print([].pop())

if __name__ == '__main__':
    try:
        msg = sys.argv[1]
    except:
        msg = '禮拜五！！！'
    wind = ' '
    for num in nums:
        time.sleep(0.06)
        print(wind * num + msg)
