import unittest
from redis import Redis
from message_queue import MessageQueue
from group import Group

class TestGroup(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)

        self.stream = "test_stream"
        self.group = "test_group"


        # objs
        self.q = MessageQueue(self.client, self.stream)
        self.g = Group(self.client, self.stream, self.group)

        # create a empty stream key
        self.msg_id = self.q.add_message({"k":"v"})
        self.q.remove_message(self.msg_id)

    def tearDown(self):
        self.client.delete(self.stream)

    def create_group(self):
        self.g.create(0)

    def add_msg_to_stream(self):
        self.q.add_message({"k":"v"})

    def test_create(self):
        self.create_group()

        self.assertNotEqual(
            self.g.info(),
            []
        )

    def test_read_message(self):
        self.create_group()

        self.assertEqual(
            self.g.read_message("worker1", ">"),
            []
        )

        self.add_msg_to_stream()

        self.assertNotEqual(
            self.g.read_message("worker1", ">"),
            []
        )

    def test_ack_message(self):
        self.create_group()
        self.add_msg_to_stream()

        msgs = self.g.read_message("worker1", ">")

        msg_id = list(msgs[0].keys())[0]
        self.g.ack_message(msg_id)

        pending_count = self.g.info()['pending']
        self.assertEqual(
            pending_count,
            0
        )

    def test_info(self):
        self.assertEqual(
            self.g.info(),
            dict()
        )

        self.create_group()

        self.assertIsNotNone(
            self.g.info()
        )

    def test_consumer_info(self):
        self.create_group()

        self.assertEqual(
            self.g.consumer_info(),
            []
        )

        self.add_msg_to_stream()
        msgs = self.g.read_message("worker1", ">")

        self.assertNotEqual(
            self.g.consumer_info(),
            []
        )

    def test_delete_consumer(self):
        self.create_group()
        self.add_msg_to_stream()

        msgs = self.g.read_message("worker1", ">")

        self.g.delete_consumer("worker1")

        self.assertEqual(
            self.g.consumer_info(),
            []
        )

    def test_destroy_group(self):
        self.create_group()

        self.g.destroy()

        self.assertEqual(
            self.g.info(),
            dict()
        )

if __name__ == "__main__":
    unittest.main()
