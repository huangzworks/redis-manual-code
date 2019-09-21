class Lottery:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add_player(self, user):
        """
        将用户添加到抽奖名单当中。
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
        return self.client.srandmember(self.key, number)
