#coding:utf-8

import unittest

from redis import Redis
from shorty_url_with_cache import ShortyUrl

class TestShortyUrl(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.shorty_url = ShortyUrl(self.client)

        self.url = "RedisGuide.com"

    def test_shorten_works(self):
        short_id = self.shorty_url.shorten(self.url)
        self.assertEqual(
            self.shorty_url.restore(short_id),
            self.url
        )

    def test_shorten_cache_works(self):
        first_short_id = self.shorty_url.shorten(self.url)
        second_short_id = self.shorty_url.shorten(self.url)

        self.assertEqual(
            first_short_id,
            second_short_id
        )

    def test_restore_return_None_when_url_not_exists(self):
        self.assertIsNone(
            self.shorty_url.restore("10086")
        )


if __name__ == "__main__":
    unittest.main()
