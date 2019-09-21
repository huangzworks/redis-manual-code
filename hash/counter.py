class Counter:

    def __init__(self, client, hash_key, counter_name):
        self.client = client
        self.hash_key = hash_key
        self.counter_name = counter_name

    def increase(self, n=1):
        """
        将计数器的值加上 n ，然后返回计数器当前的值。
        如果用户没有显式地指定 n ，那么将计数器的值加上一。
        """
        return self.client.hincrby(self.hash_key, self.counter_name, n)

    def decrease(self, n=1):
        """
        将计数器的值减去 n ，然后返回计数器当前的值。
        如果用户没有显式地指定 n ，那么将计数器的值减去一。
        """
        return self.client.hincrby(self.hash_key, self.counter_name, -n)

    def get(self):
        """
        返回计数器的当前值。
        """
        value = self.client.hget(self.hash_key, self.counter_name)
        # 如果计数器并不存在，那么返回 0 作为默认值。
        if value is None:
            return 0
        else:
            return int(value)

    def reset(self):
        """
        将计数器的值重置为 0 。
        """
        self.client.hset(self.hash_key, self.counter_name, 0)
