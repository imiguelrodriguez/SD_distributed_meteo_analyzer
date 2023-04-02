import redis


class Proxy:
    MAX_SECONDS = 4

    def __init__(self):
        self._r = redis.Redis(host="localhost", port=6379)
        pass

    def tumblingWindow(self):
        pass

