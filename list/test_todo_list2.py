#coding:utf-8

import unittest

from redis import Redis
from todo_list2 import Event, TodoList

class TestEvent(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.event_id = "10086"

        self.title = "hello"
        self.content = "this is peter speaking!"
        self.category = "message"
        self.due_date = "2016-12-6"

        self.event = Event(self.client, self.event_id)

    def test_set(self):
        self.assertTrue(
            self.event.set(self.title, self.content, self.category, self.due_date)
        )

    def test_get(self):
        self.event.set(self.title, self.content, self.category, self.due_date)
        self.assertEqual(
            self.event.get(),
            {"id": self.event_id, 
             "title": self.title,
             "content": self.content,
             "category": self.category,
             "due_date": self.due_date}
        )

class TestTodoList(unittest.TestCase):

    def setUp(self):
        self.client = Redis()
        self.client.flushdb()

        self.todolist_id = "12345"
        self.title = "hello"
        self.content = "this is peter speaking!"
        self.category = "message"
        self.due_date = "2016-12-6"

        self.todolist = TodoList(self.client, self.todolist_id)

    def test_add(self):
        self.assertIsNotNone(
            self.todolist.add(self.title, self.content, self.category, self.due_date)
        )

    def test_show_todo_list(self):
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )
        event_id = self.todolist.add(self.title, self.content, self.category, self.due_date)
        self.assertEqual(
            self.todolist.show_todo_list(),
            [str(event_id)]
        )

    def test_remove(self):
        event_id = self.todolist.add(self.title, self.content, self.category, self.due_date)
        self.todolist.remove(event_id)
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )

    def test_show_done_list_and_done(self):
        self.assertEqual(
            self.todolist.show_done_list(),
            []
        )
        event_id = self.todolist.add(self.title, self.content, self.category, self.due_date)
        self.todolist.done(event_id)
        self.assertEqual(
            self.todolist.show_done_list(),
            [str(event_id)]
        )
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )

if __name__ == "__main__":
    unittest.main()
