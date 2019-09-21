def following_key(user):
    return user + "::following"

def recommend_follow_key(user):
    return user + "::recommend_follow"

class RecommendFollow:

    def __init__(self, client, user):
        self.client = client
        self.user = user

    def calculate(self, seed_size):
        """
        计算并储存用户的推荐关注数据。
        """
        # 1)从用户关注的人中随机选一些人作为种子用户
        user_following_set = following_key(self.user)
        following_targets = self.client.srandmember(user_following_set, seed_size)
        # 2)收集种子用户的正在关注集合键名
        target_sets = set()
        for target in following_targets:
            target_sets.add(following_key(target))
        # 3)对所有种子用户的正在关注集合执行并集计算，并储存结果
        return self.client.sunionstore(recommend_follow_key(self.user), *target_sets)

    def fetch_result(self, number):
        """
        从已有的推荐关注数据中随机地获取指定数量的推荐关注用户。
        """
        return self.client.srandmember(recommend_follow_key(self.user), number)

    def delete_result(self):
        """
        删除已计算出的推荐关注数据。
        """
        self.client.delete(recommend_follow_key(self.user))
