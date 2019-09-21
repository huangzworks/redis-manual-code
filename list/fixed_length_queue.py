#coding:utf-8

def max_length_key(list_key):
    return list_key + "::max_length"

class FixedLengthQueue:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def set_max_length(self, max_length):
        """
        设置队列的最大长度。
        """
        key = max_length_key(self.key)
        self.client.set(key, max_length)

    def get_max_length(self):
        """
        获取队列的最大长度。
        """
        key = max_length_key(self.key)
        none_or_number_in_str = self.client.get(key)
        if none_or_number_in_str is not None:
            return int(none_or_number_in_str)

    def enqueue(self, item):
        """
        尝试将一个元素推入到队列里面，并在推入操作执行成功时返回 True ；
        如果队列包含的元素数量已经超过最大限制，那么推入操作执行失败，返回 False 。
        """
        # 获取队列的最大长度，并且确保最大长度已经设置
        max_length = self.get_max_length()
        assert(max_length is not None)
        # 将新元素推入到列表
        rpush_result = self.client.rpush(self.key, item)
        # 对列表进行修剪，移除那些超出列表长度限制的元素
        self.client.ltrim(self.key, 0, max_length-1)
        # 判断此次推入的元素是否被保留在列表里面（没有被 LTRIM 删掉）
        length_after_push = int(rpush_result)
        if length_after_push > max_length:
            return False
        else:
            return True

    def dequeue(self):
        """
        弹出并返回队列开头的元素。
        """
        return self.client.lpop(self.key)

    def len(self):
        """
        返回队列的长度。
        """
        return self.client.llen(self.key)
