class Like:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def cast(self, user):
        """
        用户尝试进行点赞。
        如果此次点赞执行成功，那么返回 True ；
        如果用户之前已经点过赞，那么返回 False 表示此次点赞无效。
        """
        return self.client.sadd(self.key, user) == 1

    def undo(self, user):
        """
        取消用户的点赞。
        """
        self.client.srem(self.key, user)

    def is_liked(self, user):
        """
        检查用户是否已经点过赞。
        是的话返回 True ，否则的话返回 False 。
        """
        return self.client.sismember(self.key, user)

    def get_all_liked_users(self):
        """
        返回所有已经点过赞的用户。
        """
        return self.client.smembers(self.key)

    def count(self):
        """
        返回已点赞用户的人数。
        """
        return self.client.scard(self.key)
