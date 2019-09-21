#coding:utf-8

from redis import WatchError

class Lock:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def acquire(self, identifier):
        """
        尝试获取锁，并设置一个解锁时使用的身份标识符，
        获取锁成功是返回 True ，失败时返回 False 。
        """
        true_or_none = self.client.set(self.key, identifier, nx=True)
        return true_or_none is True

    def release(self, identifier):
        """
        使用获取锁时设置的标识符去尝试释放锁，
        标识符正确并且成功释放锁时返回 True ，
        标识符不正确导致未能释放锁时返回 False ，
        如果锁并不存在，那么返回 None 表示解锁操作没有执行。
        """
        # 开启事务
        pipe = self.client.pipeline()
        while True:
            try:
                # 监视作为锁的键
                pipe.watch(self.key)
                # 获取锁当前的标识符
                current_identifier = pipe.get(self.key)
                # 根据标识符执行相应的动作
                if current_identifier is None:
                    pipe.unwatch()
                    return None
                elif current_identifier == identifier:
                    pipe.multi()
                    pipe.delete(self.key)
                    pipe.execute()
                    return True
                else:
                    # current_identifier != identifier
                    pipe.unwatch()
                    return False
            except WatchError:
                # 如果操作的过程中锁键的值被修改了
                # 那么自动进行重试，直到操作执行成功为止
                continue
            finally:
                # Python 客户端在使用 WATCH 命令时会导致连接池中的某个连接被绑定
                # 因此在执行完 WATCH 之后需要调用 reset() 方法将被绑定的连接释放到连接池里面
                pipe.reset()
