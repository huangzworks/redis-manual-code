import unittest

from time import sleep

from redis import Redis
from timing_lock import TimingLock

class TestTimingLock(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.lock = TimingLock(self.client, "test-lock")

        self.timeout = 3

    def tearDown(self):
        self.client.flushdb()

    def test_lock_is_unique(self):
        self.assertTrue(
            self.lock.acquire(self.timeout)
        )

        self.assertFalse(
            self.lock.acquire(self.timeout)
        )

    def test_release(self):
        self.assertFalse(
            self.lock.release()
        )

        self.lock.acquire(self.timeout)
        
        self.assertTrue(
            self.lock.release()
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
        print("创建了一个 {0} 秒后自动释放的锁：".format(self.timeout))
        i = self.timeout
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
