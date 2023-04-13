import asyncio
import argparse
import time


async def job(msg, sleep, name):
    print(f'== {name}開始 ==')
    await asyncio.sleep(sleep)
    print(msg)


async def pull(num, msg='hello'):
    print(f'== {num}開始 ==')
    await asyncio.sleep(10)
    print(num + ' ' + msg)


async def main(msg='hello'):
    # 老測試
    job1 = job(msg, 2, '一號測試')
    job2 = job('world', 2, '二號測試')
    await asyncio.gather(job1, job2)

    # 新測試
    await pull(msg)


######################
#     new test       #
######################
loop = asyncio.get_event_loop()


def request(url):
    """模擬 SERVER 響應"""
    time.sleep(3)
    print(f'== {url} 響應成功 ==')
    return '200'


async def request_job():
    """模擬發請求"""
    url = 'http://27c4-1-163-221-80.ngrok.io/hello'
    resp = await loop.run_in_executor(None, request, url)
    print(resp)


def new_main():
    jobs = [request_job() for _ in range(5)]
    print(jobs)
    loop.run_until_complete(asyncio.wait(jobs))


if __name__ == '__main__':
    # 舊的測試
    # asyncio.run(main('kkk'))

    # 新測試
    # 輸入參數
    # loop = asyncio.get_event_loop()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--name', type=str)
    # args = parser.parse_args()
    # loop.run_until_complete(main(args.name))

    # New main test
    new_main()
