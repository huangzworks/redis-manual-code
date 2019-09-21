#coding:utf-8

class Lottery:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add_player(self, user):
        """
        将用户添加到抽奖活动当中。
        """
        self.client.sadd(self.key, user)

    def get_all_players(self):
        """
        返回参加抽奖活动的所有用户。
        """
        return self.client.smembers(self.key)

    def player_count(self):
        """
        返回参加抽奖活动的用户人数。
        """
        return self.client.scard(self.key)

    def draw(self, number):
        """
        抽取指定数量的获奖者。
        """
        # 因为 redis-py 目前还不支持 SPOP 命令的 count 参数
        # 所以我们在这里只能通过调用多次 SPOP  命令来获得多个随机元素
        winners = list()
        for i in range(number):
            winners.append(self.client.spop(self.key))
        return winners
