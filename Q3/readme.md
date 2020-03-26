# Geo-distributed-LRU-cache

The cache is based on redis, so it is resilient to network failures or crashes, and writing on redis are considered in real time, so the writes are in real time. Data consistenc is covered as the data is always consistent in redis. Locality of reference is covered by using IP address to get the geolocation, and than calculate the distance between server and clent, finally, choose the server which is closest to the client. Cache can expire. The time of each data written or queried is also recoded in database, so when we query database, we can know if the cache is expired. If the cache is expired, the cache will be deleted and return none.

## LRU Cache Implementation

To create the LRU logic were necessary to use the following collections, data structures and tools:

### OrderedDict

An ordereddict is a dictionary in which the key is recorded in sequence.

### Redis

Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries and streams.

### This library use HASHes

Redis HASHes store a mapping of keys to values. The values that can be stored in HASHes are the same as what can be stored as normal STRINGs: strings themselves.

Note: This in order to maintain the data backed on a in-memory database and speed up the writes and replications.

### Urllib

urllib is a package that collects several modules for working with URLs, urllib.request is used for opening and reading URLs. By openning specific URLs, we can know the IP address of client.

### Geopy

Geopy is a Python 2 and 3 client for several popular geocoding web services. Geopy.geodesic can be used for calculating the distance between two location.

### Life cycle of the methods

#### life-cycle of a PUT:

1. The item is created/updated on the OrderedDict. Each key is mapped to a tuple which contains value and time. The capacity of the cache should be given to validates the capacity of the cache.
2. Remove the Last Recently Used key by using the popitem() command if no more space is found and key is not in cache. The capacity of the cache should be given.If the key has been in OrderedDict, first pop(key), then put the key into OrderedDict again to keep the sequence.
3. LRU cache is updated , make sure the redis database is consistant with local OrderedDict.
4. Ttl(Time to live) should be given, the item will expire in that amount of time in the next put funtion or get function using.

#### life-cycle of a GET:

1. If the key is not in cachem return None. 
2. Use pop(key) to get the value anf time. If it's expired, return None.
3. Put the key into cache again to keep the sequence and change the time, return the value.

## Usage

```python
from Q3.DistributedCache import DistributedCache
import time


cache = DistributedCache(max_len=128, max_age_seconds=60, redis_host='localhost', redis_port=6379, redis_db=0, cache_name='lrucache')
cache.put('a', '1')
cache.get('a')  # return '1'
time.sleep(5)
cache.get('a')  # return None
```

 Where:

```
max_len: The capacity of the cache instance (128 by default)
max_age_seconds: time to live, the expiration time 
cache_name: The name of the cache instance to create ('lrucache' by default)
redis_host: The host name of redis server ('localhost' by default)
redis_port: The port of redis server (6379 by default)
redis_db: The database to use on redis (0 by default)
```

methods:

```
put: To create a cache item into the cache instance should have an extra argument (max_age_seconds) to expire this specific item
get: The obtain a cache item altering the order of the items
add_server: Add an available server, the cache would be connected to closest server
clear: To clear the entire cache instance
```

