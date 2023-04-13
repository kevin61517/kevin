import asyncio
import requests


loop = asyncio.get_event_loop()


async def job():
    print(f'== 阿亮伺服器測試開始 ==')
    url = 'http://27c4-1-163-221-80.ngrok.io/hello'
    payload = {}
    resp = await loop.run_in_executor(None, requests.get, url)
    print(resp)


def main():
    jobs = [job() for _ in range(5)]
    loop.run_until_complete(asyncio.wait(jobs))


if __name__ == '__main__':
    # 舊的測試
    main()
