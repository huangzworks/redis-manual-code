#coding:utf-8

class Stack:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def push(self, item):
        """
        将给定的元素推入到栈中，然后返回栈当前包含的元素数量。
        """
        return self.client.lpush(self.key, item)

    def pop(self):
        """
        弹出最新被推入到栈中的元素。
        """
        return self.client.lpop(self.key)

    def count(self):
        """
        返回栈当前包含的元素数量。
        """
        return self.client.llen(self.key)
