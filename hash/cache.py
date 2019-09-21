#coding:utf-8

class Cache:

    def __init__(self, client, hash):
        self.client = client
        self.hash = hash

    def set(self, field, value):
        """
        将给定的值缓存到散列的指定字段中。
        """
        self.client.hset(self.hash, field, value)

    def get(self, field):
        """
        从散列的指定字段中获取被缓存的值，
        如果值不存在，那么返回 None 。
        """
        return self.client.hget(self.hash, field)

    def is_exists(self, field):
        """
        检查给定的字段是否储存了缓存值，
        是的话返回 True ，否则的话返回 False 。
        """
        return self.client.hexists(self.hash, field)

    def size(self):
        """
        返回散列目前已缓存的值数量。
        """
        return self.client.hlen(self.hash)

    def delete(self, field):
        """
        从散列中删除指定字段储存的缓存值，
        删除成功时返回 True ，因为缓存值不存在而导致删除失败时返回 False 。
        """
        return self.client.hdel(self.hash, field) == 1
