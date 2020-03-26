from urllib.request import urlopen
from json import load
from geopy.distance import geodesic
from Q3.LRUCache import LRUCache
from Q3.RedisCache import RedisCache


class DistributedCache(LRUCache):
    def __init__(self, max_len=128, max_age_seconds=60, redis_host='localhost'):
        super().__init__(max_len, max_age_seconds)
        self.servers = []
        self.loc = self.get_Location()
        self.cur_distance = float('inf') if redis_host == 'localhost' else self.get_Distance(redis_host)

    def get_Location(self, ip=None):
        """return a tuple of latitude and longitude"""
        if not ip:
            url = 'http://ipinfo.io/json'
        else:
            url = 'http://ipinfo.io/' + ip + '/json'
        response = urlopen(url)
        data = load(response)
        loc = data['loc']
        loc = loc.split(',')
        loc = [float(i) for i in loc]
        loc = tuple(loc)
        return loc

    def get_Distance(self, sever_ip):
        """return the distance between sever and client"""
        sever_loc = self.get_Location(sever_ip)
        return geodesic(self.loc, sever_loc).km

    def add_server(self, redis_host, cache_name='lrucache', redis_port=6379, redis_db=0):
        """add a available server, if the new sever is closet to client then change the server"""
        sever_distance = self.get_Distance(redis_host)
        self.servers.append((cache_name, redis_host, redis_port, redis_db, sever_distance))
        if sever_distance < self.cur_distance:
            cache_name, redis_host, redis_port, redis_db, self.cur_distance = self.servers[0]
            self.redis_conn = RedisCache(cache_name, redis_host, redis_port, redis_db)