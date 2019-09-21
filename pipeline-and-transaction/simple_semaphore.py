#coding:utf-8

from redis import WatchError

def get_int_size(client, key):
    result = client.get(key)
    if result is None:
        return 0
    else:
        return int(result)

class Semaphore:

    def __init__(self, client, name):
        self.client = client
        self.name = name
        # 一个字符串键，用于记录当前已被获取的信号量数量
        self.counter_key = "semaphore::" + name + "::counter"
        # 一个字符串键，用于记录信号量的最大可获取数量
        self.size_key = "semaphore::" + name + "::max_size"

    def set_max_size(self, size):
        """
        设置信号量的最大可获取数量。
        """
        self.client.set(self.size_key, size)

    def get_max_size(self):
        """
        返回信号量的最大可获取数量。
        """
        return get_int_size(self.client, self.size_key)

    def get_current_size(self):
        """
        返回目前已被获取的信号量数量。
        """
        return get_int_size(self.client, self.counter_key)

    def acquire(self):
        """
        尝试获取一个信号量，成功时返回 True ，失败时返回 False 。

        如果调用该方法时 max_size 尚未被设置，那么引发一个 TypeError 。
        """
        # 开启流水线
        pipe = self.client.pipeline()
        try:
            # 监视与信号量有关的两个键
            pipe.watch(self.counter_key, self.size_key)

            # 取得当前已被获取的信号量数量，以及最大可获取的信号量数量
            current_size = get_int_size(pipe, self.counter_key)
            max_size_in_str = pipe.get(self.size_key)
            if max_size_in_str is None:
                raise TypeError("Semaphore max size not set")
            else:
                max_size = int(max_size_in_str)

            if current_size < max_size:
                # 还有剩余的信号量可用，尝试获取它
                pipe.multi()
                pipe.incr(self.counter_key)
                pipe.execute()
                return True
            else:
                # 没有信号量可用，获取失败
                return False
        except WatchError:
            # 获取过程中有其他客户端修改了 size_key 或者 counter_key ，获取失败
            return False
        finally:
            # 取消监视
            pipe.unwatch()
            # 将连接归还给连接池
            pipe.reset()

    def release(self):
        """
        尝试释放一个信号量，返回 True 表示释放成功，
        返回 False 表示没有信号量可供释放，又或者释放操作执行失败。
        """
        # 开启流水线
        pipe = self.client.pipeline()
        try:
            # 监视 counter 键
            pipe.watch(self.counter_key)

            # 取得当前已被获取的信号量数量
            current_size = get_int_size(pipe, self.counter_key)

            # 检查是否有信号量可供释放
            if current_size > 0:
                pipe.multi()
                pipe.decr(self.counter_key)
                pipe.execute()
                return True
            else:
                return False
        except WatchError:
            # 释放过程中有其他客户端修改了 counter_key ，释放失败
            return False
        finally:
            # 取消监视
            pipe.unwatch()
            # 将连接归还给连接池
            pipe.reset()
