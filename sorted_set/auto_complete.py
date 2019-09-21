class AutoComplete:

    def __init__(self, client):
        self.client = client

    def feed(self, content, weight=1):
        """
        根据用户输入的内容构建自动补全结果，
        其中 content 参数为内容本身，而可选的 weight 参数则用于指定内容的权重值。
        """
        for i in range(1, len(content)):
            key = "auto_complete::" + content[:i]
            self.client.zincrby(key, weight, content)

    def hint(self, prefix, count):
        """
        根据给定的前缀 prefix ，获取 count 个自动补全结果。
        """
        key = "auto_complete::" + prefix
        return self.client.zrevrange(key, 0, count-1)
