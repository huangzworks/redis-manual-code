class Timeline:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add(self, item, time):
        """
        将元素添加到时间线里面。
        """
        self.client.zadd(self.key, {item:time})

    def remove(self, item):
        """
        从时间线里面移除指定元素。
        """
        self.client.zrem(self.key, item)

    def count(self):
        """
        返回时间线包含的元素数量。
        """
        return self.client.zcard(self.key)

    def pagging(self, number, count, with_time=False):
        """
        按照每页 count 个元素计算，取出时间线第 number 页上的所有元素，
        这些元素将根据时间戳逆序排列。
        如果可选参数 with_time 的值为 True ，那么元素对应的时间戳也会一并被返回。
        注意：number 参数的起始值是 1 而不是 0 。
        """
        start_index = (number - 1)*count
        end_index = number*count-1
        return self.client.zrevrange(self.key, start_index, end_index, withscores=with_time) 

    def fetch_by_time_range(self, min_time, max_time, number, count, with_time=False):
        """
        按照每页 count 个元素计算，获取指定时间段第 number 页上的所有元素，
        这些元素将根据时间戳逆序排列。
        如果可选参数 with_time 的值为 True ，那么元素对应的时间戳也会一并被返回。
        注意：number 参数的起始值是 1 而不是 0 。
        """
        start_index = (number-1)*count
        return self.client.zrevrangebyscore(self.key, max_time, min_time, start_index, 
                                            count, withscores=with_time)
