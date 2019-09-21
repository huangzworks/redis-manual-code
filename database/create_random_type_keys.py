import random

def create_random_type_keys(client, number):
    """
    在数据库中创建指定数量的类型随机键。
    """
    for i in range(number):
        # 构建键名
        key = "key:{0}".format(i)
        # 从六个键创建函数中随机选择一个
        create_key_func = random.choice([
            create_string, 
            create_hash, 
            create_list, 
            create_set, 
            create_zset, 
            create_stream
        ])
        # 实际地创建键
        create_key_func(client, key)

def create_string(client, key):
    client.set(key, "")

def create_hash(client, key):
    client.hset(key, "", "")

def create_list(client, key):
    client.rpush(key, "")

def create_set(client, key):
    client.sadd(key, "")

def create_zset(client, key):
    client.zadd(key, {"":0})

def create_stream(client, key):
    client.xadd(key, {"":""})
