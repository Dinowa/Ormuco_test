import time
from threading import RLock
from Q3.RedisCache import RedisCache
from collections import OrderedDict


class LRUCache(OrderedDict):
    def __init__(self, max_len=128, max_age_seconds=60, redis_host='localhost', redis_port=6379, redis_db=0, cache_name='lrucache'):
        super().__init__()
        assert max_age_seconds >= 0
        assert max_len >= 1

        self.max_len = max_len  # the capacity
        self.max_age = max_age_seconds
        self.lock = RLock()
        self.redis_conn = RedisCache(cache_name, redis_host, redis_port, redis_db)
        self.get_items_from_cache()  # get the former cache from database

    def __contains__(self, key):
        """ Return True if the dict has a key, else return False. """
        try:
            with self.lock:
                item = OrderedDict.__getitem__(self, key)
                if time.time() - item[1] < self.max_age:
                    return True
                else:
                    del self[key]
                    self.redis_conn.remove(key)
        except KeyError:
            pass
        return False

    def __getitem__(self, key):
        """ Return the item of the dict.
        Raises a KeyError if key is not in the map.
        """
        with self.lock:
            cur_time = time.time()
            item = OrderedDict.__getitem__(self, key)
            item_age = cur_time - item[1]
            if item_age < self.max_age:
                return item[0]
            else:
                del self[key]
                self.redis_conn.remove(key)
                raise KeyError(key)

    def __setitem__(self, key, value, cur_time=time.time()):
        """ Set d[key] to value. """
        with self.lock:
            if key not in self:
                if len(self) == self.max_len:
                    try:
                        first = next(iter(self))
                        if first in self:
                            self.pop(first)
                    finally:
                        self.redis_conn.remove(first)
            else:
                if len(self) == self.max_len:
                    OrderedDict.pop(self, key)
                    self.redis_conn.remove(key)
            OrderedDict.__setitem__(self, key, (value, cur_time))
            self.redis_conn.set(key, value, cur_time)

    def set_capacity(self, n: int) -> None:
        """ reset the capacity of the LRU"""
        self.max_len = n
        while len(self) > self.max_len:
            deleted = self.popitem(last=False)
            del self[deleted]
            self.redis_conn.remove(deleted)

    def get_items_from_cache(self):
        """get the former cache from database"""
        OrderedDict.clear(self)
        for key, value in self.redis_conn.get_all_keys().items():
            if not key.endswith('_time?'):
                self.__setitem__(key, value, float(self.redis_conn.get(key + '_time?')))

    def set_redis_conn(self, redis, cache_name):
        """reset the redis connection"""
        self.redis_conn = RedisCache(cache_name=cache_name)
        self.redis_conn.set_redis_conn(redis)
        self.get_items_from_cache()

    def get(self, key, default=None):
        try:
            cur_time = time.time()
            value = self.__getitem__(key)
            del self[key]
            OrderedDict.__setitem__(self, key, (value, cur_time))
            self.redis_conn.set(key, value, cur_time)
            return value
        except KeyError:
            return default

    def put(self, key, value):
        self.__setitem__(key, value)

    def clear(self):
        OrderedDict.clear(self)
        self.redis_conn.clear()