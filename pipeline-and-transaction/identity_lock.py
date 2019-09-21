from redis import WatchError

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
        # 开启流水线
        pipe = self.client.pipeline()
        try:
            # 监视锁键
            pipe.watch(self.key)
            # 获取锁键储存的标识符
            lock_identity = pipe.get(self.key)
            if lock_identity is None:
                # 如果锁键的标识符为空，那么说明锁已经被释放
                return True
            elif input_identity == lock_identity:
                # 如果给定的标识符与锁键储存的标识符相同，那么释放这个锁
                # 为了确保 DEL 命令在执行时的安全性，我们需要使用事务去包裹它
                pipe.multi()
                pipe.delete(self.key)
                pipe.execute()
                return True
            else:
                # 如果给定的标识符与锁键储存的标识符并不相同
                # 那么说明当前客户端不是锁的持有者
                # 拒绝本次释放请求
                return False
        except WatchError:
            # 抛出异常说明在 DEL 命令执行之前，已经有其他客户端修改了锁键
            return False
        finally:
            # 取消对键的监视
            pipe.unwatch()
            # 因为 redis-py 在执行 WATCH 命令期间，会将流水线与单个连接进行绑定
            # 所以在执行完 WATCH 命令之后，必须调用 reset() 方法将连接归还给连接池
            pipe.reset()
