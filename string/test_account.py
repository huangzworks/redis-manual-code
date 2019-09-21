#coding:utf-8

import unittest

from redis import Redis
from account import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.account_id = "32595"

        self.username = "happy_jack"
        self.email = "happy_jack@spammail.com"
        self.password = "888168"

        self.account = Account(self.client, self.account_id)

    def test_create_works(self):
        self.assertTrue(
            self.account.create(self.username, self.email, self.password)
        )

        self.assertIsNotNone(
            self.account.get()
        )

    def test_create_return_false_when_account_exists(self):
        self.account.create(self.username, self.email, self.password)

        self.assertFalse(
            self.account.create(self.username, self.email, self.password)
        )

    def test_get_works(self):
        self.account.create(self.username, self.email, self.password)

        data = self.account.get()

        self.assertEqual(
            data["id"],
            self.account_id
        )
        self.assertEqual(
            data["username"],
            self.username
        )
        self.assertEqual(
            data["password"],
            self.password
        )
        self.assertIsNotNone(
            data["created_at"]
        )

    def test_update_works(self):
        self.account.create(self.username, self.email, self.password)

        new_password = "123888"

        self.assertTrue(
            self.account.update(password=new_password)
        )

        data = self.account.get()

        self.assertEqual(
            data["password"],
            new_password
        )

if __name__ == "__main__":
    unittest.main()
