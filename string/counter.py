class Counter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def increase(self, n=1):
        """
        将计数器的值加上 n ，然后返回计数器当前的值。
        如果用户没有显式地指定 n ，那么将计数器的值加上一。
        """
        return self.client.incr(self.key, n)

    def decrease(self, n=1):
        """
        将计数器的值减去 n ，然后返回计数器当前的值。
        如果用户没有显式地指定 n ，那么将计数器的值减去一。
        """
        return self.client.decr(self.key, n)

    def get(self):
        """
        返回计数器当前的值。
        """
        # 尝试获取计数器当前的值
        value = self.client.get(self.key)
        # 如果计数器并不存在，那么返回 0 作为计数器的默认值
        if value is None:
            return 0
        else:
            # 因为 redis-py 的 get() 方法返回的是字符串值
            # 所以这里需要使用 int() 函数，将字符串格式的数字转换为真正的数字类型
            # 比如将 "10" 转换为 10
            return int(value)

    def reset(self):
        """
        清零计数器，并返回计数器在被清零之前的值。
        """
        old_value = self.client.getset(self.key, 0)
        # 如果计数器之前并不存在，那么返回 0 作为它的旧值
        if old_value is None:
            return 0
        else:
            # 跟 redis-py 的 get() 方法一样， getset() 方法返回的也是字符串值
            # 所以程序在将计数器的旧值返回给调用者之前，需要先将它转换成真正的数字
            return int(old_value)
