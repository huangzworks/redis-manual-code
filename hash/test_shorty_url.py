#coding:utf-8

import unittest

from redis import Redis
from shorty_url import ShortyUrl

class TestShortyUrl(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.shorty_url = ShortyUrl(self.client)

        self.url = "RedisGuide.com"

    def test_shorten_works(self):
        short_id = self.shorty_url.shorten(self.url)
        self.assertEqual(
            self.shorty_url.restore(short_id),
            self.url
        )

    def test_restore_return_None_when_url_not_exists(self):
        self.assertIsNone(
            self.shorty_url.restore("10086")
        )


if __name__ == "__main__":
    unittest.main()
