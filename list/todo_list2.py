#coding:utf-8

def make_event_key(event_id):
    return "TodoList::event::" + str(event_id)

def make_todolist_key(user_id):
    return "TodoList::todo_events::" + str(user_id)

def make_donelist_key(user_id):
    return "TodoList::done_events::" + str(user_id)


class Event:

    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.key = make_event_key(id)

    def set(self, title, content="", category="", due_date=""):
        """
        设置待办事项的各项信息，并在设置成功时返回 True 。
        """
        data = {
            "title": title,
            "content": content,
            "category": category,
            "due_date": due_date
        }
        return self.client.hmset(self.key, data)

    def get(self):
        """
        获取待办事项的各项信息，并以字典方式返回这些信息。
        """
        # 获取信息
        event_data = self.client.hgetall(self.key)
        # 将待办事项的 ID 也添加到被返回的信息中，方便查询
        event_data["id"] = self.id
        return event_data


class TodoList:

    def __init__(self, client, user_id):
        self.client = client
        # 根据用户的 ID ，创建出代办事项列表和已完成事项列表
        self.todolist = make_todolist_key(user_id)
        self.donelist = make_donelist_key(user_id)
        # 待办事项的 ID 生成器
        self.event_id = "TodoList::event_id"

    def add(self, title, content="", category="", due_date=""):
        """
        添加新的待办事项，并返回该事项的 ID 。
        """
        # 为新的待办事项生成 ID
        new_event_id = self.client.incr(self.event_id)
        # 设置待办事项的相关信息
        new_event = Event(self.client, new_event_id)
        new_event.set(title, content, category, due_date)
        # 将待办事项的 ID 添加到待办事项列表中
        self.client.rpush(self.todolist, new_event_id)
        return new_event_id

    def remove(self, event_id):
        """
        移除指定的待办事项，
        移除成功时返回 True ，失败时返回 False 。
        """
        self.client.lrem(self.todolist, event_id, 0)

    def done(self, event_id):
        """
        将指定的待办事项设置为已完成。
        """
        self.client.lrem(self.todolist, event_id, 0)
        self.client.lpush(self.donelist, event_id)

    def show_todo_list(self):
        """
        列出用户的所有待办事项的 ID 。
        """
        return self.client.lrange(self.todolist, 0, -1)

    def show_done_list(self):
        """
        列出用户的所有已完成事项的 ID 。
        """
        return self.client.lrange(self.donelist, 0, -1)
