import unittest

from time import sleep
from redis import Redis
from boardcast import Boardcast
from threading import Thread

class TestBoardcast(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)

        self.topic = "news"

        self.b = Boardcast(self.client, self.topic) 

        self.msg = "Zed is dead baby, Zed is dead."

    def tearDown(self):
        self.b.close()

    def test_publish(self):
        self.b.publish(self.msg)
        self.assertIsNotNone(
            self.b.listen()
        )

    def test_subscribe(self):
        self.b.publish(self.msg)
        self.assertEqual(
            self.b.listen(),
            self.msg
        )
        print("Sleep one second to test the blocking feature...")
        self.assertIsNone(
            self.b.listen(1)
        )

    def test_status(self):
        self.assertEqual(
            self.b.status(),
            1
        )

    def test_close(self):
        self.b.close()
        self.assertEqual(
            self.b.status(),
            0
        )

if __name__ == "__main__":
    unittest.main()
