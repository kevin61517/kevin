def aaa(n: int) -> int:
    if n <= 3:
        return n
    origin: list = [1, 2]
    for i in range(int(n)):
        origin.append(origin[-1] + origin[-2])
    print(origin[n-1])


if __name__ == '__main__':
    aaa(4)


v9 = 'DISABLED_PLATFORMS = "DT,LH,CR,BBIN,BBINSport,BBINSlot,BBINLottery,BBINFish,BB,BBSport,BBSlot,BBLottery,BBFish,BBLive,JDB,SABAH,TTG,OG,HG,IBO,PT,OBPoker,OBG,OBSport,IGSlot,DS,WL,WLPoker,WLFish,WLLive,ZutouSport,XBB,XBBSlot"'
y9 = 'DISABLED_PLATFORMS = "DT,LH,CR,BBIN,BBINSport,BBINSlot,BBINLottery,BBINFish,BB,BBSport,BBSlot,BBLottery,BBFish,BBLive,JDB,SABAH,TTG,OG,HG,IBO,PT,OBPoker,OBG,OBSport,IGSlot,DS,WL,WLPoker,WLFish,WLLive,ZutouSport,XBB,XBBSlot"'