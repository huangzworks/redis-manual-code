#coding:utf-8

import random
from time import time

RADIUS_CACHE_TIME = 60
USER_LOCATION_KEY = "user_location"

def make_cache_radius_key(user, radius):
    return "cached_radius::{0}::{1}".format(user, radius)

def make_last_cache_time_key(user, radius):
    return "last_cache_time::{0}::{1}".format(user, radius)

class Location:

    def __init__(self, client):
        self.client = client
        self.key = USER_LOCATION_KEY

    def pin(self, user, longitude, latitude):
        """
        记录指定用户的坐标。
        """
        self.client.geoadd(self.key, longitude, latitude, user)

    def get(self, user):
        """
        获取指定用户的坐标。
        """
        position_list = self.client.geopos(self.key, user)
        # geopos() 允许用户输入多个用户，然后以列表形式返回各个用户的坐标
        # 因为我们这里只传入了一个用户，所以只需要取出列表的第一个元素即可
        if position_list != []:
            return position_list[0]

    def calculate_distance(self, user_a, user_b):
        """
        以公里为单位，计算两个用户之间的直线距离。
        """
        return self.client.geodist(self.key, user_a, user_b, unit="km")

    def find_nearby(self, user, radius=1):
        """
        以公里为单位，寻找并返回 user 指定半径范围内的所有其他用户。
        """
        # 检查缓存的更新时间，并在有需要时删除已过期的缓存
        cache_key = make_cache_radius_key(user, radius)                 # 缓存查找结果的键
        last_cache_time_key = make_last_cache_time_key(user, radius)    # 记录缓存最后更新时间的键
        last_cache_time = self.client.get(last_cache_time_key)          # 缓存的最后更新时间
        current_time = time()                                           # 当前时间
        if (last_cache_time is not None) and (float(last_cache_time)+RADIUS_CACHE_TIME < current_time):
            # 缓存已过期，删除它
            self.client.delete(cache_key)

        # 尝试获取已缓存的查找结果，并在结果可用时，直接返回它
        cached_result = self.client.lrange(cache_key, 0, -1)
        if cached_result != []:
            return cached_result

        # 没有缓存可用，进行实际的查找，并将结果缓存起来，最后向调用者返回结果
        result = self.client.georadiusbymember(self.key, user, radius, unit="km")   # 获取附近的所有用户
        all_nearby_users = filter(lambda other_user: other_user != user, result)    # 移除结果中的 user 自身
        if all_nearby_users != []:
            # 缓存查找结果
            self.client.rpush(cache_key, *all_nearby_users)
            # 修改缓存的最后更新时间
            self.client.set(last_cache_time_key, current_time) 
        # 返回结果
        return all_nearby_users

    def find_random_nearby(self, user, radius=1):
        """
        以公里为单位，随机地返回一个位于 user 指定半径内的其他用户。
        """
        # random.choice() 方法用于从列表中随机地选择并返回一个项
        return random.choice(self.find_nearby(user, radius))
