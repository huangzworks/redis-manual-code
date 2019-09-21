#coding:utf-8

import unittest

from redis import Redis
from todo_list import TodoList

class TestTodoList(unittest.TestCase):

    def setUp(self):
        self.client = Redis(decode_responses=True)
        self.client.flushdb()

        self.todolist = TodoList(self.client, "peter")

        self.events = ["buy some milk", 
                       "have lunch", 
                       "watch tv",
                       "finish homework", 
                       "go to sleep"]

    def test_add(self):
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )
        self.todolist.add(self.events[0])
        self.assertNotEqual(
            self.todolist.show_todo_list(),
            []
        )

    def test_remove(self):
        self.todolist.add(self.events[0])
        self.todolist.remove(self.events[0])
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )

    def test_done(self):
        self.todolist.add(self.events[0])
        self.todolist.done(self.events[0])
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )
        self.assertNotEqual(
            self.todolist.show_done_list(),
            []
        )

    def test_show_todo_list(self):
        self.assertEqual(
            self.todolist.show_todo_list(),
            []
        )

        for event in self.events:
            self.todolist.add(event)

        self.assertEqual(
            self.todolist.show_todo_list(),
            list(reversed(self.events))
        )

    def test_show_done_list(self):
        self.assertEqual(
            self.todolist.show_done_list(),
            []
        )

        for event in self.events:
            self.todolist.add(event)

        for event in self.events:
            self.todolist.done(event)

        self.assertEqual(
            self.todolist.show_done_list(),
            list(reversed(self.events))
        )

if __name__ == "__main__":
    unittest.main()
