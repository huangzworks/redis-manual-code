#coding:utf-8

from random import random
from hashlib import sha256

DEFAULT_TIMEOUT = 3600*24*30    # one month

def create_session_key(uid):
    return "login_session::" + str(uid)

def encrypt_alogrithm(uid):
    content = str(random()) + str(uid)
    return sha256(content).hexdigest()

class LoginSession:

    def __init__(self, client, uid):
        self.client = client
        self.uid = uid
        self.key = create_session_key(self.uid)

    def generate(self, timeout=DEFAULT_TIMEOUT):
        """
        生成并返回新的登录会话。
        """
        token = encrypt_alogrithm(self.uid)
        self.client.set(self.key, token)
        self.client.expire(self.key, timeout)
        return token
        
    def validate(self, input_token):
        """
        验证会话令牌的正确性，
        函数在目标会话不存在时返回 -2 ，令牌不正确时返回 -1 ，令牌正确时返回 0 。
        """
        right_token = self.client.get(self.key)
        if right_token is None:
            return -2
        elif input_token != right_token:
            return -1
        else:
            return 0

    def remain_valid_time(self):
        """
        返回会话的剩余有效时间。
        """
        return self.client.ttl(self.key)

    def destroy(self):
        """
        销毁指定的会话。
        """
        self.client.delete(self.key)
