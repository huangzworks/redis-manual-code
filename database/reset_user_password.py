import random

from redis import Redis
from hashlib import sha256

def generate_new_password():
    random_string = str(random.getrandbits(256)).encode('utf-8')
    return sha256(random_string).hexdigest()

def reset_user_password(origin, new):
    # 两个客户端，分别连接两个数据库
    origin_db = Redis(db=origin)
    new_db = Redis(db=new)

    for key in origin_db.scan_iter(match="user::*"):
        # 从源数据库获取现有用户信息
        user_data = origin_db.hgetall(key)
        # 重置用户密码
        user_data["password"] = generate_new_password()
        # 将新的用户信息储存到新数据库里面
        new_db.hmset(key, user_data)

    # 互换新旧数据库
    origin_db.swapdb(origin, new)

    # 以异步方式移除旧数据库
    # （new_db 变量现在已经指向旧数据库）
    new_db.flushdb(asynchronous=True)
