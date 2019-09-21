import unittest

from time import sleep

from redis import Redis
from volatile_cache import VolatileCache

class TestVolatileCache(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.cache = VolatileCache(self.client)

        self.key = "message"
        self.value = "hello world"
        self.timeout = 1

    def test_set_and_get(self):
        self.cache.set(self.key, self.value, self.timeout)

        self.assertEqual(
            self.cache.get(self.key),
            self.value
        )

    def test_get_return_none_when_key_not_exist(self):
        self.assertIsNone(
            self.cache.get(self.key)
        )

    def test_cache_will_delete_after_timeout(self):
        self.cache.set(self.key, self.value, self.timeout)

        print("正在测试缓存的过期特性，等待{0}秒钟……".format(self.timeout))
        sleep(self.timeout+1) # 增加一秒钟，避免误差

        self.assertIsNone(
            self.cache.get(self.key)
        )

        print("缓存已被自动删除！")

if __name__ == "__main__":
    unittest.main()
