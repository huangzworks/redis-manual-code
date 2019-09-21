class Boardcast:

    def __init__(self, client, topic):
        self.client = client
        self.topic = topic
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.topic)
        # 丢弃频道的订阅消息
        # 为了确保程序能收到订阅消息，故设置一秒钟的超时时限
        self.pubsub.get_message(timeout=1)

    def publish(self, content):
        """
        针对主题发布给定的内容。
        """
        self.client.publish(self.topic, content)

    def listen(self, timeout=0):
        """
        在给定的时限内监听与主题有关的内容。
        """
        result = self.pubsub.get_message(timeout=timeout)
        if result is not None:
            return result["data"] # 只返回消息正文

    def status(self):
        """
        查看主题当前的订阅量。
        """
        result = self.client.pubsub_numsub(self.topic)
        return result[0][1] # 只返回订阅量，丢弃频道的名字

    def close(self):
        """
        停止广播。
        """
        self.pubsub.unsubscribe(self.topic)
