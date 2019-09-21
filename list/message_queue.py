class MessageQueue:

    def __init__(self, client, queue_name):
        self.client = client
        self.queue_name = queue_name

    def add_message(self, message):
        """
        将一条消息放入到队列里面。
        """
        self.client.rpush(self.queue_name, message)

    def get_message(self, timeout=0):
        """
        从队列里面获取一条消息，
        如果暂时没有消息可用，那么就在 timeout 参数指定的时限内阻塞并等待可用消息出现。

        timeout 参数的默认值为 0 ，表示一直等待直到消息出现为止。
        """
        # blpop 的结果可以是 None ，也可以是一个包含两个元素的元组
        # 元组的第一个元素是弹出元素的来源队列，而第二个元素则是被弹出的元素
        result = self.client.blpop(self.queue_name, timeout)
        if result is not None:
            source_queue, poped_item = result
            return poped_item

    def len(self):
        """
        返回队列目前包含的消息数量。
        """
        return self.client.llen(self.queue_name)
