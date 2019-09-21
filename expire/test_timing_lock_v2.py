#coding:utf-8

import unittest

from time import sleep

from redis import Redis
from timing_lock_v2 import TimingLock

class TestTimingLock(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.lock = TimingLock(self.client, "test-lock")

        self.timeout = 3000 # 3000 毫秒

    def test_lock_is_unique(self):
        self.assertTrue(
            self.lock.acquire(self.timeout)
        )

        self.assertFalse(
            self.lock.acquire(self.timeout)
        )

    def test_lock_is_available_after_release(self):
        self.lock.acquire(self.timeout)

        self.lock.release()

        self.assertTrue(
            self.lock.acquire(self.timeout)
        )

    def test_lock_will_release_after_reach_timeout(self):
        self.lock.acquire(self.timeout)
        
        print("")  # 隔开上面测试的输出
        print("创建了一个 {0} 毫秒后自动释放的锁，请稍等：".format(self.timeout))

        i = 3
        while i != 0:
            print("倒数 {0} 秒钟……".format(i))
            sleep(1)
            i -= 1

        self.assertTrue(
            self.lock.acquire(self.timeout)
        )

        print("锁已自动被释放！")


if __name__ == "__main__":
    unittest.main()
