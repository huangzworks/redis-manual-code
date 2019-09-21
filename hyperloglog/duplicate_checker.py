class DuplicateChecker:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def is_duplicated(self, content):
        """
        在信息重复时返回 True ，未重复时返回 False 。
        """
        return self.client.pfadd(self.key, content) == 0

    def unique_count(self):
        """
        返回检查器已经检查过的非重复信息数量。
        """ 
        return self.client.pfcount(self.key)
