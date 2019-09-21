import unittest

from redis import Redis
from mlpop import mlpop

class TestMlpop(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.list_key = "lst"

    def tearDown(self):
        self.client.flushdb()

    def test_mlpop_return_nones_when_list_empty(self):
        self.assertEqual(
            mlpop(self.client, self.list_key, 3),
            [None, None, None]
        )

    def test_mlpop_return_items_when_list_not_empty(self):
        items = ["123", "456", "789"]
        self.client.rpush(self.list_key, *items)

        self.assertEqual(
            mlpop(self.client, self.list_key, 3),
            items
        )


if __name__ == "__main__":
    unittest.main()
