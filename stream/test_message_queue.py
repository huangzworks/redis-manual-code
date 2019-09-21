import unittest
from redis import Redis
from message_queue import MessageQueue

class TestMessageQueue(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)

        self.stream_key = "test_message_queue"
        self.q = MessageQueue(self.client, self.stream_key) 

        self.message = {"name":"peter", "age":"36", "location":"UK"}
        
        self.tearDown()

    def tearDown(self):
        self.client.delete(self.stream_key)

    def make_a_none_empty_queue(self, queue, size):
        for i in range(size):
            key = "key{0}".format(i)
            value = "value{0}".format(i)
            self.q.add_message({key:value,})

    def test_add_message(self):
        message_id = self.q.add_message(self.message)
        self.assertIsNotNone(message_id)

    def test_add_message_return_utf8_id(self):
        message_id = self.q.add_message(self.message)
        self.assertIsInstance(message_id, str)

    def test_get_message_return_none_when_msg_not_exists(self):
        self.assertIsNone(self.q.get_message("10086-0"))

    def test_get_message_return_msg_when_its_exists(self):
        message_id = self.q.add_message(self.message)
        self.assertEqual(
            self.message, 
            self.q.get_message(message_id)
        )

    def test_remove_message(self):
        message_id = self.q.add_message(self.message)
        
        self.q.remove_message(message_id)

        self.assertIsNone(self.q.get_message(message_id))

    def test_len_return_zero_when_queue_empty(self):
        self.assertEqual(self.q.len(), 0)

    def test_len_retrun_non_zero_when_queue_not_empty(self):
        id = self.q.add_message(self.message)
        self.assertEqual(self.q.len(), 1)
        self.q.remove_message(id)
        self.assertEqual(self.q.len(), 0)

    def test_get_by_range_return_empty_list_when_queue_empty(self):
        self.assertEqual(self.q.get_by_range("-", "+"), list())

    def test_get_by_range_return_none_empty_list_when_queue_not_empty(self):
        self.make_a_none_empty_queue(self.q, 10)
        result = self.q.get_by_range("-", "+")
        self.assertEqual(len(result), 10)
        self.assertEqual(type(result), list)
        for msg in result:
            self.assertEqual(type(msg), dict)

    def test_get_by_range_return_right_size(self):
        self.make_a_none_empty_queue(self.q, 10)
        result = self.q.get_by_range("-", "+", 5)
        self.assertEqual(len(result), 5)

    def test_get_by_range_return_empty_list_when_stream_empty(self):
        self.assertEqual(
            self.q.get_by_range("-", "+"),
            list()
        )

    def test_iterate_return_right_size(self):
        self.make_a_none_empty_queue(self.q, 10)
        self.assertEqual(
            len(self.q.iterate(0, 5)),
            5
        )
        self.assertEqual(
            len(self.q.iterate(0, 10)),
            10
        )

    def test_iterate_return_right_message(self):
        self.make_a_none_empty_queue(self.q, 10)
        full_message_list = self.q.get_by_range("-", "+", 10)
        self.assertEqual(
            self.q.iterate(0, 5),
            full_message_list[0:5]
        )
        self.assertEqual(
            self.q.iterate(0, 10),
            full_message_list
        )

    def test_iterate_return_empty_list_when_stream_empty(self):
        self.assertEqual(
            self.q.iterate(0),
            list()
        )

if __name__ == "__main__":
    unittest.main()
