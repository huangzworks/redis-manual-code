#coding:utf-8

class AutoComplete:

    def __init__(self, client):
        self.client = client

    def feed(self, content, weight=1, timeout=None):
        """
        根据用户输入的内容构建自动补全结果，
        其中 content 参数为内容本身，
        而可选的 weight 参数则用于指定内容的权重值，
        至于可选的 timeout 参数则用于指定自动补全结果的保存时长（单位为秒）。
        """
        transaction = self.client.pipeline()  # 开启一个事务流水线
        for i in range(1, len(content)):
            key = "auto_complete::" + content[:i]
            transaction.zincrby(key, content, weight)  # 将 ZINCRBY 命令放入到事务流水线里面
            if timeout is not None:
                transaction.expire(key, timeout)  # 将 EXPIRE 命令放入到事务流水线里面
        transaction.execute()  # 执行事务流水线中包含的所有命令

    def hint(self, prefix, count):
        """
        根据给定的前缀 prefix ，获取 count 个自动补全结果。
        """
        key = "auto_complete::" + prefix
        return self.client.zrevrange(key, 0, count-1)
