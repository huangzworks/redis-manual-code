#coding:utf-8

class FIFOqueue:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def enqueue(self, item):
        """
        将一个元素放入到队列当中，然后返回队列当前包含的元素数量。
        """
        return self.client.lpush(self.key, item)

    def dequeue(self):
        """
        弹出并返回最先被放入到队列中的元素。
        """
        return self.client.rpop(self.key)
