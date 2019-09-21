class Limiter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def set_max_execute_times(self, max_execute_times):
        """
        设置操作的最大可执行次数。
        """
        self.client.set(self.key, max_execute_times)

    def still_valid_to_execute(self):
        """
        检查是否可以继续执行被限制的操作。
        是的话返回 True ，否则返回 False 。
        """
        num = self.client.decr(self.key)
        return (num >= 0)

    def remaining_execute_times(self):
        """
        返回操作的剩余可执行次数。
        """
        num = int(self.client.get(self.key))
        if num < 0:
            return 0
        else:
            return num
