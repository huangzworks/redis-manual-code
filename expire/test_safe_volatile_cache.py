#coding:utf-8

from time import sleep
from redis import Redis
from safe_volatile_cache import VolatileCache

r = Redis()
r.flushdb()

cache = VolatileCache(r)

# 缓存文本数据

key = "message"
value = "hello world"

cache.put(key, value)

assert(
    cache.get(key) == value
)

r.flushdb()

# 缓存二进制数据

file_name = "redis-logo.jpg"

with open(file_name) as logo:
    logo_data = logo.read()

cache.put(file_name, logo_data)

assert(
    cache.get(file_name) == logo_data
)

r.flushdb()

# 测试缓存的过期性质

timeout = 3
print("为缓存设置 {0} 秒钟的过期时间。".format(timeout))
cache.put(key, value, timeout)
assert(
    cache.get(key) == value
)
left_seconds = timeout
while left_seconds != 0:
    print("倒计时 {0} 秒钟，等待缓存过期……".format(left_seconds))
    left_seconds -= 1
    sleep(1)
print("{0} 秒钟已过，缓存已被删除。".format(timeout))
assert(
    cache.get(key) is None
)

r.flushdb()

#

print("all tests passed!")
