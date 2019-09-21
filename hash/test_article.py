#coding:utf-8

import unittest

from redis import Redis
from article import Article

class TestArticle(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.id = "10086"
        self.title = "greeting"
        self.content = "hello world"
        self.author = "peter"

        self.article = Article(self.client, self.id)

    def test_create_works(self):
        self.assertTrue(
            self.article.create(self.title, self.content, self.author)
        )

        self.assertIsNotNone(
            self.article.get()
        )

    def test_get_works(self):
        self.article.create(self.title, self.content, self.author)

        data = self.article.get()
        
        self.assertEqual(
            data["id"],
            self.id
        )
        self.assertEqual(
            data["title"],
            self.title
        )
        self.assertEqual(
            data["content"],
            self.content
        )
        self.assertEqual(
            data["author"],
            self.author
        )
        self.assertIsNotNone(
            data["create_at"]
        )

    def test_create_return_false_when_id_exists(self):
        self.article.create(self.title, self.content, self.author)
        self.assertFalse(
            self.article.create(self.title, self.content, self.author)
        )

    def test_update_works(self):
        self.article.create(self.title, self.content, self.author)

        new_title = "new message"

        self.assertTrue(
            self.article.update(title=new_title)
        )

        data = self.article.get()

        self.assertEqual(
            new_title,
            data["title"]
        )

if __name__ == "__main__":
    unittest.main()
