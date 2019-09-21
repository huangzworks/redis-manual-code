#coding:utf-8

class Limiter:

    def __init__(self, client, limiter_name):
        self.client = client
        self.max_execute_times_key = limiter_name + '::max_execute_times'
        self.current_execute_times_key = limiter_name + '::current_execute_times'

    def set_max_execute_times(self, n):
        """
        设置操作的最大可执行次数。
        """
        self.client.set(self.max_execute_times_key, n)
        # 初始化操作的已执行次数为 0
        self.client.set(self.current_execute_times_key, 0)

    def get_max_execute_times(self):
        """
        返回操作的最大可执行次数。
        """
        return int(self.client.get(self.max_execute_times_key))

    def get_current_execute_times(self):
        """
        返回操作的当前已执行次数。
        """
        current_execute_times = int(self.client.get(self.current_execute_times_key))
        max_execute_times = self.get_max_execute_times()

        if current_execute_times > max_execute_times:
            # 当用户尝试执行操作的次数超过最大可执行次数时
            # current_execute_times 的值就会比 max_execute_times 的值更大
            # 为了将已执行次数的值保持在 
            # 0 <= current_execute_times <= max_execute_times 这一区间
            # 如果已执行次数已经超过最大可执行次数
            # 那么程序将返回最大可执行次数作为结果
            return max_execute_times
        else:
            # 否则的话，返回真正的当前已执行次数作为结果
            return current_execute_times

    def still_valid_to_execute(self):
        """
        检查是否可以继续执行被限制的操作，
        是的话返回 True ，不是的话返回 False 。
        """
        updated_current_execute_times = self.client.incr(self.current_execute_times_key)
        max_execute_times = self.get_max_execute_times()
        return (updated_current_execute_times <= max_execute_times)

    def remaining_execute_times(self):
        """
        返回操作的剩余可执行次数。
        """
        current_execute_times = self.get_current_execute_times()
        max_execute_times = self.get_max_execute_times()
        return max_execute_times - current_execute_times

    def reset_current_execute_times(self):
        """
        清零操作的已执行次数。
        """
        self.client.set(self.current_execute_times_key, 0)
