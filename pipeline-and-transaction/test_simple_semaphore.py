#coding:utf-8

import unittest

from redis import Redis
from simple_semaphore import Semaphore

class TestSemaphore(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.semaphore = Semaphore(self.client, "test-semaphore")

        self.max_size = 3

    def test_raise_type_error_when_max_size_not_set(self):
        with self.assertRaises(TypeError):
            self.semaphore.acquire()

    def test_set_max_size_and_get_max_size(self):
        self.semaphore.set_max_size(self.max_size)

        self.assertEqual(
            self.semaphore.get_max_size(),
            self.max_size
        )

        self.semaphore.set_max_size(10)
        self.assertEqual(
            self.semaphore.get_max_size(),
            10
        )

    def test_get_current_size(self):
        self.semaphore.set_max_size(self.max_size)

        self.assertEqual(
            self.semaphore.get_current_size(),
            0
        )

        self.semaphore.acquire()

        self.assertEqual(
            self.semaphore.get_current_size(),
            1
        )

        self.semaphore.release()

        self.assertEqual(
            self.semaphore.get_current_size(),
            0
        )

    def test_acquire_and_release_works(self):
        self.semaphore.set_max_size(self.max_size)

        self.assertTrue(
            self.semaphore.acquire()
        )
        self.assertTrue(
            self.semaphore.release()
        )

    def test_acquire_return_false_when_reach_max_size(self):
        self.semaphore.set_max_size(self.max_size)

        for i in range(self.max_size):
            self.assertTrue(
                self.semaphore.acquire()
            )

        self.assertFalse(
            self.semaphore.acquire()
        )

if __name__ == "__main__":
    unittest.main()
