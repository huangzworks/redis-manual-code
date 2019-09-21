def make_tag_key(item):
    return item + "::tags"

class Tagging:

    def __init__(self, client, item):
        self.client = client
        self.key = make_tag_key(item)

    def add(self, *tags):
        """
        为对象添加一个或多个标签。
        """
        self.client.sadd(self.key, *tags)

    def remove(self, *tags):
        """
        移除对象的一个或多个标签。
        """
        self.client.srem(self.key, *tags)

    def is_included(self, tag):
        """
        检查对象是否带有给定的标签，
        是的话返回 True ，不是的话返回 False 。
        """
        return self.client.sismember(self.key, tag)

    def get_all_tags(self):
        """
        返回对象带有的所有标签。
        """
        return self.client.smembers(self.key)

    def count(self):
        """
        返回对象带有的标签数量。
        """
        return self.client.scard(self.key)
