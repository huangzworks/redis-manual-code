#coding:utf-8

from redis import Redis
from lock import Lock
from uuid import uuid4

client = Redis()
client.flushdb()

lock = Lock(client, 'test-lock')

identifier = str(uuid4())

# acquire test

assert(
    lock.acquire(identifier) is True
)

assert(
    lock.acquire('another-identifier') is False
)

# release test

assert(
    lock.release("another-identifier") is False
)

assert(
    lock.release(identifier) is True
)

assert(
    lock.release("lock is empty now") is None
)

# acquire after release test

assert(
    lock.acquire(identifier) is True
)

#

client.flushdb()
print("all tests passed!")
