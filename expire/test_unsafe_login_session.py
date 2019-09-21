#coding:utf-8

from redis import Redis
from unsafe_login_session import LoginSession

client = Redis()
client.flushdb()

uid = "peter"

session = LoginSession(client, uid)

#

token = session.generate()
assert(
    token is not None
)

#

assert(
    session.validate(token) == 0
)
assert(
    session.validate("wrong-token") == -1
)

#

assert(
    session.remain_valid_time() > 0
)

session.destroy()

assert(
    session.remain_valid_time() < 0
)

assert(
    session.validate("wrong-token") == -2
)

#

client.flushdb()
print("all tests passed!")
