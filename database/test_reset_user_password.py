import unittest

from redis import Redis
from reset_user_password import *

class TestRestUserPassword(unittest.TestCase):

    def clean_db(self):
        self.client = Redis()
        self.client.flushall()

    def setUp(self):
        self.clean_db()

        self.origin = 0
        self.new = 1

    def tearDown(self):
        self.clean_db()

    def test_reset_user_password(self):
        user_key = "user::256"
        old_password ="12345"

        self.client.hmset(
            user_key, 
            {
                "email": "hi@spam.com", 
                "password": old_password
            }
        )

        reset_user_password(self.origin, self.new)

        db0 = Redis(db=self.origin,decode_responses=True)
        db1 = Redis(db=self.new)

        # 确保数据库 0 的用户密码已被更新
        self.assertNotEqual(
            db0.hgetall(user_key)["password"],
            old_password
        )
        
        # 确保数据库 1 已被清空
        self.assertEqual(
            db1.dbsize(),
            0
        )

if __name__ == "__main__":
    unittest.main()
