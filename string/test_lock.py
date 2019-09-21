#coding:utf-8

import unittest

from redis import Redis
from lock import Lock

class TestLock(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.lock = Lock(self.client, 'lock')

    def test_only_one_lock_can_be_acquire(self):
        self.assertTrue(
            self.lock.acquire()
        )
        self.assertFalse(
            self.lock.acquire()
        )

    def test_release_works(self):
        self.lock.acquire()
        self.assertTrue(
            self.lock.release()
        )

    def test_release_return_false_when_lock_not_acquired(self):
        self.assertFalse(
            self.lock.release()
        )

if __name__ == "__main__":
    unittest.main()
