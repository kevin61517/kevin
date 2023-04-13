import asyncio
import argparse
import time


async def job(name, sleep):
    print(f'== {name}開始 ==')
    await asyncio.sleep(sleep)
    print(f'== {name}完成 ==')
    return


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    jobs = [job('AAA', 2), job('BBB', 1)]
    a = loop.run_until_complete(asyncio.wait(jobs))
    if a:
        for item in a[0]:
            print(item.result())
