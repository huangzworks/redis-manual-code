class UniqueCounter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def count_in(self, item):
        """
        尝试将给定元素计入到计数器当中：
        如果给定元素之前没有被计数过，那么方法返回 True 表示此次计数有效；
        如果给定元素之前已经被计数过，那么方法返回 False 表示此次计数无效。
        """
        return self.client.sadd(self.key, item) == 1

    def get_result(self):
        """
        返回计数器的值。
        """
        return self.client.scard(self.key)
