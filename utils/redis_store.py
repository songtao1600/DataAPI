# -*- coding:utf-8 -*-
# @Author :songtao

import redis
from config import redis_options


class RedisStore(object):
    def __init__(self):
        # self._tick_cli = redis.StrictRedis.from_url(**redis_options)
        self._tick_cli = redis.StrictRedis(**redis_options)
        self._tick_ps = self._tick_cli.pubsub()
        pass

    def set(self, k, v):
        self._tick_cli.set(k, v)

    def get(self, k):
        return self._tick_cli.get(k)
        pass

    def publish(self, channel, msg):
        self._tick_ps.publish(channel, msg)
        pass

    def subscribe(self,channels):
        self._tick_ps.subscribe(channels)
        pass

    def expire(self, k, ttl):
        self._tick_cli.expire(k, ttl)
        pass
