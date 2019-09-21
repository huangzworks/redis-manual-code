import random
from time import time  # 获取浮点数格式的 unix 时间戳
from hashlib import sha256

# 会话的默认过期时间
DEFAULT_TIMEOUT = 3600*24*30    # 一个月

# 储存会话令牌以及会话过期时间戳的散列
SESSION_TOKEN_HASH = "session::token"
SESSION_EXPIRE_TS_HASH = "session::expire_timestamp"

# 会话状态
SESSION_NOT_LOGIN = "SESSION_NOT_LOGIN"
SESSION_EXPIRED = "SESSION_EXPIRED"
SESSION_TOKEN_CORRECT = "SESSION_TOKEN_CORRECT"
SESSION_TOKEN_INCORRECT = "SESSION_TOKEN_INCORRECT"

def generate_token():
    """
    生成一个随机的会话令牌。
    """
    random_string = str(random.getrandbits(256)).encode('utf-8')
    return sha256(random_string).hexdigest()


class LoginSession:

    def __init__(self, client, user_id):
        self.client = client
        self.user_id = user_id

    def create(self, timeout=DEFAULT_TIMEOUT):
        """
        创建新的登录会话并返回会话令牌，
        可选的 timeout 参数用于指定会话的过期时间（以秒为单位）。
        """
        # 生成会话令牌
        user_token = generate_token()
        # 计算会话到期时间戳
        expire_timestamp = time()+timeout
        # 以用户 ID 为字段，将令牌和到期时间戳分别储存到两个散列里面
        self.client.hset(SESSION_TOKEN_HASH, self.user_id, user_token)
        self.client.hset(SESSION_EXPIRE_TS_HASH, self.user_id, expire_timestamp)
        # 将会话令牌返回给用户
        return user_token

    def validate(self, input_token):
        """
        根据给定的令牌验证用户身份。
        这个方法有四个可能的返回值，分别对应四种不同情况：
        1. SESSION_NOT_LOGIN —— 用户尚未登录
        2. SESSION_EXPIRED —— 会话已过期
        3. SESSION_TOKEN_CORRECT —— 用户已登录，并且给定令牌与用户令牌相匹配
        4. SESSION_TOKEN_INCORRECT —— 用户已登录，但给定令牌与用户令牌不匹配
        """
        # 尝试从两个散列里面取出用户的会话令牌以及会话的过期时间戳
        user_token = self.client.hget(SESSION_TOKEN_HASH, self.user_id)
        expire_timestamp = self.client.hget(SESSION_EXPIRE_TS_HASH, self.user_id)

        # 如果会话令牌或者过期时间戳不存在，那么说明用户尚未登录
        if (user_token is None) or (expire_timestamp is None):
            return SESSION_NOT_LOGIN

        # 将当前时间戳与会话的过期时间戳进行对比，检查会话是否已过期
        # 因为 HGET 命令返回的过期时间戳是字符串格式的
        # 所以在进行对比之前要先将它转换成原来的浮点数格式
        if time() > float(expire_timestamp):
            return SESSION_EXPIRED

        # 用户令牌存在并且未过期，那么检查它与给定令牌是否一致
        if input_token == user_token:
            return SESSION_TOKEN_CORRECT
        else:
            return SESSION_TOKEN_INCORRECT

    def destroy(self):
        """
        销毁会话。
        """
        # 从两个散列里面分别删除用户的会话令牌以及会话的过期时间戳
        self.client.hdel(SESSION_TOKEN_HASH, self.user_id)
        self.client.hdel(SESSION_EXPIRE_TS_HASH, self.user_id)
