#coding:utf-8

from cache import Cache
from base36 import base10_to_base36

ID_COUNTER = "ShortyUrl::id_counter"
URL_HASH = "ShortyUrl::url_hash" 
URL_CACHE = "ShortyUrl::url_cache"

class ShortyUrl:

    def __init__(self, client):
        self.client = client
        self.cache = Cache(self.client, URL_CACHE)  # 创建缓存对象

    def shorten(self, target_url):
        """
        为目标网址创建一个短网址 ID 。
        """
        # 尝试在缓存里面寻找目标网址对应的短网址 ID
        cached_short_id = self.cache.get(target_url)
        if cached_short_id is not None:
            return cached_short_id

        new_id = self.client.incr(ID_COUNTER)
        short_id = base10_to_base36(new_id)
        self.client.hset(URL_HASH, short_id, target_url)
        # 在缓存里面关联起目标网址和短网址 ID
        # 这样程序就可以在用户下次输入相同的目标网址时
        # 直接重用已有的短网址 ID
        self.cache.set(target_url, short_id)
        return short_id

    def restore(self, short_id):
        """
        根据给定的短网址 ID ，返回与之对应的目标网址。
        """
        return self.client.hget(URL_HASH, short_id)
