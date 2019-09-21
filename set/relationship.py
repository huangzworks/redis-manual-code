def following_key(user):
    return user + "::following"

def follower_key(user):
    return user + "::follower"

class Relationship:

    def __init__(self, client, user):
        self.client = client
        self.user = user

    def follow(self, target):
        """
        关注目标用户。
        """
        # 把 target 添加到当前用户的正在关注集合里面
        user_following_set = following_key(self.user)
        self.client.sadd(user_following_set, target)
        # 把当前用户添加到 target 的关注者集合里面
        target_follower_set = follower_key(target)
        self.client.sadd(target_follower_set, self.user)

    def unfollow(self, target):
        """
        取消对目标用户的关注。
        """
        # 从当前用户的正在关注集合中移除 target
        user_following_set = following_key(self.user)
        self.client.srem(user_following_set, target)
        # 从 target 的关注者集合中移除当前用户
        target_follower_set = follower_key(target)
        self.client.srem(target_follower_set, self.user)

    def is_following(self, target):
        """
        检查当前用户是否正在关注目标用户，
        是的话返回 True ，否则返回 False 。
        """
        # 如果 target 存在于当前用户的正在关注集合中
        # 那么说明当前用户正在关注 target
        user_following_set = following_key(self.user)
        return self.client.sismember(user_following_set, target)

    def get_all_following(self):
        """
        返回当前用户正在关注的所有人。
        """
        user_following_set = following_key(self.user)
        return self.client.smembers(user_following_set)

    def get_all_follower(self):
        """
        返回当前用户的所有关注者。
        """
        user_follower_set = follower_key(self.user)
        return self.client.smembers(user_follower_set)

    def count_following(self):
        """
        返回当前用户正在关注的人数。
        """
        user_following_set = following_key(self.user)
        return self.client.scard(user_following_set)

    def count_follower(self):
        """
        返回当前用户的关注者人数。
        """
        user_follower_set = follower_key(self.user)
        return self.client.scard(user_follower_set)
