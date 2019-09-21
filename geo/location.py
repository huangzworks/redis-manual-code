import random

USER_LOCATION_KEY = "user_locations"

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
        # geopos() 允许用户输入多个位置，然后以列表形式返回各个位置的坐标。
        # 因为我们这里只传入了一个位置，所以只需要取出列表的第一个元素即可。
        if len(position_list) != 0:
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
        all_nearby_users = self.client.georadiusbymember(self.key, user, radius, unit="km")
        # 因为 georadiusbymember() 方法会把 user 本身也包含在结果里面，
        # 但由于我们并不需要这个用户，所以使用 remove() 方法移除他
        all_nearby_users.remove(user)
        return all_nearby_users

    def find_random_nearby(self, user, radius=1):
        """
        以公里为单位，随机地返回一个位于 user 指定半径范围内的其他用户。
        """
        # random.choice() 方法用于从列表中随机地选择并返回一个项
        return random.choice(self.find_nearby(user, radius))
