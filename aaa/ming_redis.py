class Redis:
    def __init__(self):
        self._db = {}

    def set(self, key, value):
        self._db[key] = value
        return 1

    def get(self, key):
        return self._db.get(key, None)

    def hset(self, name, key, value):
        if isinstance(value, dict):
            self._db[name] = value
        else:
            self._db[name] = {key: value}
        return 1

    def hget(self, name, key):
        if self._db.get(name):
            return self._db[name].get(key)
        return 0


redis = Redis()

if __name__ == '__main__':
    key = 'loveming'
    redis.set(key, 1)
    print(redis.get(key))

