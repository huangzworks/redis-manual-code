VALUE_OF_LOCK = "locking"

class TimingLock:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def acquire(self, timeout):
        """
        尝试获取一个带有秒级最大使用时限的锁，
        成功时返回 True ，失败时返回 False 。
        """
        result = self.client.set(self.key, VALUE_OF_LOCK, ex=timeout, nx=True)
        return result is not None

    def release(self):
        """
        尝试释放锁。
        成功时返回 True ，失败时返回 False 。 
        """
        return self.client.delete(self.key) == 1
