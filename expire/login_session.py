import random
from hashlib import sha256

# 会话的默认过期时间
DEFAULT_TIMEOUT = 3600*24*30    # 一个月

# 会话状态
SESSION_NOT_LOGIN_OR_EXPIRED = "SESSION_NOT_LOGIN_OR_EXPIRED"
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
        self.key = "user::{0}::token".format(user_id)

    def create(self, timeout=DEFAULT_TIMEOUT):
        """
        创建新的登录会话并返回会话令牌，
        可选的 timeout 参数用于指定会话的过期时间（以秒为单位）。
        """
        # 生成会话令牌
        token = generate_token()
        # 储存令牌，并为其设置过期时间
        self.client.set(self.key, token, ex=timeout)
        # 返回令牌
        return token

    def validate(self, input_token):
        """
        根据给定的令牌验证用户身份。
        这个方法有三个可能的返回值，分别对应三种不同情况：
        1. SESSION_NOT_LOGIN_OR_EXPIRED —— 用户尚未登录或者令牌已过期
        2. SESSION_TOKEN_CORRECT —— 用户已登录，并且给定令牌与用户令牌相匹配
        3. SESSION_TOKEN_INCORRECT —— 用户已登录，但给定令牌与用户令牌不匹配
        """
        # 获取用户令牌
        user_token = self.client.get(self.key)
        # 令牌不存在
        if user_token is None:
            return SESSION_NOT_LOGIN_OR_EXPIRED
        # 令牌存在并且未过期，那么检查它与给定令牌是否一致
        if input_token == user_token:
            return SESSION_TOKEN_CORRECT
        else:
            return SESSION_TOKEN_INCORRECT

    def destroy(self):
        """
        销毁会话。
        """
        self.client.delete(self.key)
