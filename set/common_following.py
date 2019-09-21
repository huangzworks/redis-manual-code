def following_key(user):
    return user + "::following"

class CommonFollowing:

    def __init__(self, client):
        self.client = client

    def calculate(self, user, target):
        """
        计算并返回当前用户和目标用户共同关注的人。
        """
        user_following_set = following_key(user)
        target_following_set = following_key(target)
        return self.client.sinter(user_following_set, target_following_set)

    def calculate_and_store(self, user, target, store_key):
        """
        计算出当前用户和目标用户共同关注的人，
        并把结果储存到 store_key 指定的键里面，
        最后返回共同关注的人数作为返回值。
        """
        user_following_set = following_key(user)
        target_following_set = following_key(target)
        return self.client.sinterstore(store_key, user_following_set, target_following_set)
