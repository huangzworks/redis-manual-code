class IdentityLock:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def acquire(self, identity, timeout):
        """
        尝试获取一个带有身份标识符和最大使用时限的锁，
        成功时返回 True ，失败时返回 False 。
        """
        result = self.client.set(self.key, identity, ex=timeout, nx=True)
        return result is not None

    def release(self, input_identity):
        """
        根据给定的标识符，尝试释放锁。
        返回 True 表示释放成功；
        返回 False 则表示给定的标识符与锁持有者的标识符并不相同，释放请求被拒绝。
        """
        # 获取锁键储存的标识符
        lock_identity = self.client.get(self.key)
        if lock_identity is None:
            # 如果锁键的标识符为空，那么说明锁已经被释放
            return True
        elif input_identity == lock_identity:
            # 如果给定的标识符与锁键的标识符相同，那么释放这个锁
            self.client.delete(self.key)
            return True
        else:
            # 如果给定的标识符与锁键的标识符并不相同
            # 那么说明当前客户端不是锁的持有者
            # 拒绝本次释放请求
            return False
