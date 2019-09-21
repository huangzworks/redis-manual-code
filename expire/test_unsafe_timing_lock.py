#coding:utf-8

from time import sleep
from redis import Redis
from unsafe_timing_lock import TimingLock

client = Redis()
lock = TimingLock(client, "timing-lock")

client.flushdb()

# 确保锁的唯一性

assert(
    lock.acquire(10) is True
)

assert(
    lock.acquire(5) is False
)

lock.release()

# 验证锁的过期功能

sleep_time = 3
print("创建一个 {0} 秒钟后自动释放的锁。".format(sleep_time))
lock.acquire(sleep_time)
while sleep_time != 0:
    print("倒数 {0} 秒钟……".format(sleep_time))
    sleep_time -= 1
    sleep(1)
assert(    # 此时锁应该已被释放，可以被获取
    lock.acquire(0) is True
)
print("已再次获取锁，证明之前的锁已自动释放。")

#

client.flushdb()
print("all tests passed!")
