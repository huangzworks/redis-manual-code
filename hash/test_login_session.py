#coding:utf-8

import unittest

from time import sleep
from redis import Redis
from login_session import LoginSession, SESSION_NOT_LOGIN, SESSION_EXPIRED, SESSION_TOKEN_CORRECT, SESSION_TOKEN_INCORRECT

class TestLoginSession(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.user_id = "peter"

        self.login_session = LoginSession(self.client, self.user_id)

    def test_generate_works(self):
        user_token = self.login_session.create()
        self.assertIsNotNone(
            user_token
        )

    def test_validate_in_case_of_SESSION_NOT_LOGIN(self):
        self.assertEqual(
            self.login_session.validate("wrong token"),
            SESSION_NOT_LOGIN
        )

    def test_validate_in_case_of_SESSION_EXPIRED(self):
        self.login_session.create(timeout=1)
        print("testing timeout function, wait 2 seconds ...")
        sleep(2)
        self.assertEqual(
            self.login_session.validate("wrong token"),
            SESSION_EXPIRED
        )

    def test_validate_in_case_of_SESSION_TOKEN_CORRECT(self):
        token = self.login_session.create()
        self.assertEqual(
            self.login_session.validate(token),
            SESSION_TOKEN_CORRECT
        )

    def test_validate_in_case_of_SESSION_TOKEN_INCORRECT(self):
        self.login_session.create()
        self.assertEqual(
            self.login_session.validate("wrong token"),
            SESSION_TOKEN_INCORRECT
        )

    def test_destroy_works(self):
        self.login_session.create()
        self.login_session.destroy()
        self.assertEqual(
            self.login_session.validate("wrong token"),
            SESSION_NOT_LOGIN
        )

if __name__ == "__main__":
    unittest.main()
