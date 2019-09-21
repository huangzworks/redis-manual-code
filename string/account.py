#coding:utf-8

from time import time

class Account:

    def __init__(self, client, account_id):
        self.client = client
        # 用户 ID
        self.id = str(account_id)
        # 储存用户信息的各个键
        self.username_key = "account::" + self.id + "::username"
        self.email_key = "account::" + self.id + "::email"
        self.password_key = "account::" + self.id + "::password"
        self.created_at_key = "account::" + self.id + "::created_at"

    def create(self, username, email, password):
        """
        创建一个新账号，创建成功时返回 True ，
        因为账号已存在而导致创建失败时返回 False 。
        """
        account_data = {
            self.username_key: username,
            self.email_key: email,
            self.password_key: password,
            self.created_at_key: time()
        }
        return self.client.msetnx(account_data)

    def get(self):
        """
        返回 ID 对应的账号信息。
        """
        result = self.client.mget(self.username_key,
                                  self.email_key,
                                  self.password_key,
                                  self.created_at_key)
        return {"id": self.id, "username": result[0], "email": result[1], "password": result[2], "created_at": result[3]}

    def update(self, email=None, password=None):
        """
        对账号信息进行更新，
        更新成功时返回 True ，更新失败时返回 False 。
        """
        account_data = {}
        if email is not None:
            account_data[self.email_key] = email
        if password is not None:
            account_data[self.password_key] = password
        return self.client.mset(account_data)
