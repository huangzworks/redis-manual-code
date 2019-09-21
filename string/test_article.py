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

    def test_get_content_len_works(self):
        self.article.create(self.title, self.content, self.author)
        self.assertEqual(
            len(self.content),
            self.article.get_content_len()
        )

    def test_get_content_preview_works(self):
        long_content = "Nor subjects, for what matters. Everybody will tell you to don't add a dot at the end of the first line of a commit message. I followed the advice for some time, but I'll stop today, because I don't believe commit messages are titles or subjects. They are synopsis of the meaning of the change operated by the commit, so they are small sentences. The sentence can be later augmented with more details in the next lines of the commit message, however many times there is *no* body, there is just the first line. How many emails or articles you see with just the subject or the title? Very little, I guess."

        self.article.create(self.title, long_content, self.author)

        self.assertEqual(
            self.article.get_content_preview(150),
            long_content[:150]
        )

if __name__ == "__main__":
    unittest.main()
