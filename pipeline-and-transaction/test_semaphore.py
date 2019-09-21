import unittest

from redis import Redis
from semaphore import Semaphore

class TestSemaphore(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.semaphore = Semaphore(self.client, "test-semaphore")

        self.max_size = 3

    def tearDown(self):
        self.client.flushdb()

    def test_raise_type_error_when_max_size_not_set(self):
        with self.assertRaises(TypeError):
            self.semaphore.acquire("huangz")

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

        self.semaphore.acquire("huangz")

        self.assertEqual(
            self.semaphore.get_current_size(),
            1
        )

        self.semaphore.release("huangz")

        self.assertEqual(
            self.semaphore.get_current_size(),
            0
        )

    def test_acquire_and_release_works(self):
        self.semaphore.set_max_size(self.max_size)

        self.assertTrue(
            self.semaphore.acquire("huangz")
        )
        self.assertTrue(
            self.semaphore.release("huangz")
        )

    def test_acquire_return_false_when_reach_max_size(self):
        self.semaphore.set_max_size(self.max_size)

        for i in range(self.max_size):
            self.assertTrue(
                self.semaphore.acquire(i)
            )

        self.assertFalse(
            self.semaphore.acquire("you acquire too much semaphore!")
        )

    def test_release_return_false_when_identity_not_match(self):
        self.semaphore.set_max_size(self.max_size)

        self.semaphore.set_max_size(self.max_size)

        self.semaphore.acquire("huangz")

        self.assertFalse(
            self.semaphore.release("wrong identity")
        )

if __name__ == "__main__":
    unittest.main()
