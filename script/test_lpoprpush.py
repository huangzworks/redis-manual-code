import unittest

from redis import Redis
from lpoprpush import lpoprpush

class TestLpoprpush(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.source = "lst1"
        self.target = "lst2"

    def tearDown(self):
        self.client.flushdb()

    def test_return_none_when_list_empty(self):
        self.assertIsNone(
            lpoprpush(self.client, self.source, self.target)
        )

    def test_works_in_same_list(self):
        self.client.rpush(self.source, "a", "b", "c")

        self.assertEqual(
            lpoprpush(self.client, self.source, self.source),
            "a"
        )

        self.assertEqual(
            self.client.lrange(self.source, 0, -1),
            ["b", "c", "a"]
        )

    def test_works_in_different_list(self):
        self.client.rpush(self.source, "a", "b", "c")
        self.client.rpush(self.target, "d", "e", "f")

        self.assertEqual(
            lpoprpush(self.client, self.source, self.target),
            "a"
        )

        self.assertEqual(
            self.client.lrange(self.source, 0, -1),
            ["b", "c"]
        )
        self.assertEqual(
            self.client.lrange(self.target, 0, -1),
            ["d", "e", "f", "a"]
        )

if __name__ == "__main__":
    unittest.main()
