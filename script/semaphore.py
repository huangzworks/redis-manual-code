#coding:utf-8

from redis import ResponseError

class Semaphore:

    def __init__(self, client, name):
        self.client = client
        self.name = name
        # 一个集合，用于储存信号量持有者的标识符
        self.holder_key = "semaphore::" + name + "::holders"
        # 一个字符串，用于记录信号量的最大可获取数量
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
        result = self.client.get(self.size_key)
        if result is None:
            return 0
        else:
            return int(result)

    def get_current_size(self):
        """
        返回目前已被获取的信号量数量。
        """
        return self.client.scard(self.holder_key)

    def acquire(self, identity):
        """
        尝试获取一个信号量，成功时返回 True ，失败时返回 False 。
        传入的 identity 参数将被用于标识客户端的身份。

        如果调用该方法时 max_size 尚未被设置，那么引发一个 TypeError 。
        """
        script = """
        local holder_key = KEYS[1]
        local size_key = KEYS[2]
        local identity = ARGV[1]
        
        -- 取得当前已被获取的信号量数量，以及最大可获取的信号量数量
        -- 通过 tonumber() 函数可以将字符串形式的数字转换为 Lua 中的 number 数字类型
        -- 如果用户尚未对 size_key 进行设置，那么 max_size 的值将被设置为 nil
        local current_size = tonumber(redis.call("SCARD", holder_key))
        local max_size = tonumber(redis.call("GET", size_key))

        -- 信号量获取操作不能在 size_key 未被设置的情况下执行
        if max_size == nil then
            return redis.error_reply("Semaphore max size not set")
        end

        -- 如果还有剩余的信号量可用，那么将给定的标识符放入到持有者集合中
        if current_size < max_size then
            return redis.call("SADD", holder_key, identity)
        end
        """
        try:
            return self.client.eval(script, 2, self.holder_key, self.size_key, identity) == 1
        except ResponseError as error:
            # 脚本中的 redis.error_reply() 调用将引发一个 ResponseError 异常
            # 为了与原来的信号量程序 API 保持一致，这里将 ResponseError 转换为 TypeError
            raise TypeError(error.message)
       
    def release(self, identity):
        """
        根据给定的标识符，尝试释放当前客户端持有的信号量。
        返回 True 表示释放成功，返回 False 表示因为标识符不匹配而导致释放失败。
        """
        # 尝试从持有者集合中移除给定的标识符
        result = self.client.srem(self.holder_key, identity)
        if result == 1:
            # 移除成功说明客户端为持有者之一，释放成功
            return True
        else:
            # 移除失败说明客户端并不是持有者，释放失败
            return False
