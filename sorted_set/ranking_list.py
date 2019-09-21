class RankingList:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def set_score(self, item, score):
        """
        为排行榜中的指定元素设置分数，不存在的元素会被添加到排行榜里面。
        """
        self.client.zadd(self.key, {item:score})

    def get_score(self, item):
        """
        获取排行榜中指定元素的分数。
        """
        return self.client.zscore(self.key, item)

    def remove(self, item):
        """
        从排行榜中移除指定的元素。
        """
        self.client.zrem(self.key, item)

    def increase_score(self, item, increment):
        """
        将给定元素的分数增加 increment 分。
        """
        self.client.zincrby(self.key, increment, item)

    def decrease_score(self, item, decrement):
        """
        将给定元素的分数减少 decrement 分。
        """
        # 因为 Redis 没有直接提供能够减少元素分值的命令
        # 所以这里通过传入一个负数减量来达到减少分值的目的
        self.client.zincrby(self.key, 0-decrement, item)

    def get_rank(self, item):
        """
        获取给定元素在排行榜中的排名。
        """
        rank = self.client.zrevrank(self.key, item)
        # 因为 Redis 元素的排名是以 0 为开始的，
        # 而现实世界中的排名通常以 1 为开始，
        # 所以这里在返回排名之前会执行加一操作。
        if rank is not None: 
            return rank+1

    def top(self, n, with_score=False):
        """
        获取排行榜中得分最高的 n 个元素，
        如果可选的 with_score 参数的值为 True ，那么将元素的分数（分值）也一并返回。
        """
        return self.client.zrevrange(self.key, 0, n-1, withscores=with_score)
