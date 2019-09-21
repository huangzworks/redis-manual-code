class UniqueCounter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def count_in(self, item):
        """
        对给定元素进行计数。
        """
        self.client.pfadd(self.key, item)

    def get_result(self):
        """
        返回计数器的值。
        """
        return self.client.pfcount(self.key)
