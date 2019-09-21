#coding:utf-8

class FixedLengthQueue:

    def __init__(self, client, key, max_length):
        self.client = client
        self.key = key
        self.max_length = max_length

    def enqueue(self, item):
        pipe = self.client.pipeline()
        pipe.rpush(self.key, item)
        pipe.ltrim(self.key, 0, self.max_length-1)
        result = pipe.execute()
        # RPUSH 命令在推入元素之后返回列表的当前长度
        # 通过判断当前长度是否大于最大长度
        # 可以判断这次推入是否有效（新推入的元素不会被 LTRIM 删除）
        length_of_queue_after_enqueue = int(result[0])
        if length_of_queue_after_enqueue > self.max_length:
            return False
        else:
            return True

    def dequeue(self):
        return self.client.lpop(self.key)

    def len(self):
        return self.client.llen(self.key)
