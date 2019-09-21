import unittest

from redis import Redis
from create_random_type_keys import *

class TestCreateRandomTypeKeys(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.key = "key"

    def tearDown(self):
        self.client.flushdb()

    def test_create_string(self):
        create_string(self.client, self.key)
        self.assertEqual(
            self.client.type(self.key),
            "string"
        )

    def test_create_hash(self):
        create_hash(self.client, self.key)
        self.assertEqual(
            self.client.type(self.key),
            "hash"
        )

    def test_create_list(self):
        create_list(self.client, self.key)
        self.assertEqual(
            self.client.type(self.key),
            "list"
        )

    def test_create_set(self):
        create_set(self.client, self.key)
        self.assertEqual(
            self.client.type(self.key),
            "set"
        )

    def test_create_zset(self):
        create_zset(self.client, self.key)
        self.assertEqual(
            self.client.type(self.key),
            "zset"
        )

    def test_create_stream(self):
        create_stream(self.client, self.key)
        self.assertEqual(
            self.client.type(self.key),
            "stream"
        )

    def test_create_random_type_keys(self):
        dbsize = 100
        create_random_type_keys(self.client, dbsize)
        self.assertEqual(
            self.client.dbsize(),
            dbsize
        )

if __name__ == "__main__":
    unittest.main()
