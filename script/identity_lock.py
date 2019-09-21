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
        返回 False 则表示给定的标识符与锁持有者的标识符不相同，释放请求被拒绝。
        """
        script = """
        -- 使用局部变量储存锁键键名以及标识符，提高脚本的可读性
        local key = KEYS[1]
        local input_identity = ARGV[1]

        -- 获取锁键储存的标识符
        -- 当标识符为空时，Lua 会将 GET 返回的 nil 转换为 false
        local lock_identity = redis.call("GET", key)

        if lock_identity == false then
            -- 如果锁键储存的标识符为空，那么说明锁已经被释放
            return true
        elseif input_identity == lock_identity then
            -- 如果给定的标识符与锁键储存的标识符相同，那么释放这个锁
            redis.call("DEL", key)
            return true
        else
            -- 如果给定的标识符与锁键储存的标识符并不相同
            -- 那么说明当前客户端不是锁的持有者，拒绝本次释放请求
            return false
        end
        """
        # 因为 Redis 会将脚本返回的 true 转换为数字 1
        # 所以这里通过检查脚本返回值是否为 1 来判断解锁操作是否成功
        result = self.client.eval(script, 1, self.key, input_identity)
        return result == 1
