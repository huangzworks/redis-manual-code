from message_queue import reconstruct_message_list, get_message_from_nested_list

class Group:
    """
    为消息队列提供消费者组功能。
    """

    def __init__(self, client, stream, group):
        self.client = client
        self.stream = stream
        self.group = group

    def create(self, start_id):
        """
        创建消费者组。
        """
        self.client.xgroup_create(self.stream, self.group, start_id)

    def destroy(self):
        """
        删除消费者组。
        """
        self.client.xgroup_destroy(self.stream, self.group)

    def read_message(self, consumer, id, count=10):
        """
        从消费者组中读取消息。
        """
        reply = self.client.xreadgroup(self.group, consumer, {self.stream: id}, count)
        if len(reply) == 0:
            return list()
        else:
            messages = get_message_from_nested_list(reply)
            return reconstruct_message_list(messages)

    def ack_message(self, id):
        """
        确认已处理完毕的消息。
        """
        self.client.xack(self.stream, self.group, id)

    def info(self):
        """
        返回消费者组的相关信息。
        """
        # 因为一个流可以拥有多个消费者组
        # 所以我们需要从命令返回的多个组信息中找到正确的信息
        for group_info in self.client.xinfo_groups(self.stream):
            if group_info['name'] == self.group:
                return group_info
        else:
            return dict()

    def consumer_info(self):
        """
        返回消费者组属下消费者的相关信息。
        """
        return self.client.xinfo_consumers(self.stream, self.group)

    def delete_consumer(self, consumer):
        """
        删除指定消费者。
        """
        self.client.xgroup_delconsumer(self.stream, self.group, consumer)
