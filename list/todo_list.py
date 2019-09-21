def make_todo_list_key(user_id):
    """
    储存待办事项的列表。
    """
    return user_id + "::todo_list"

def make_done_list_key(user_id):
    """
    储存已完成事项的列表。
    """
    return user_id + "::done_list"


class TodoList:

    def __init__(self, client, user_id):
        self.client = client
        self.user_id = user_id
        self.todo_list = make_todo_list_key(self.user_id)
        self.done_list = make_done_list_key(self.user_id)

    def add(self, event):
        """
        将指定事项添加到待办事项列表中。
        """
        self.client.lpush(self.todo_list, event)

    def remove(self, event):
        """
        从待办事项列表中移除指定的事项。
        """
        self.client.lrem(self.todo_list, 0, event)

    def done(self, event):
        """
        将待办事项列表中的指定事项移动到已完成事项列表，
        以此来表示该事项已完成。
        """
        # 从待办事项列表中移除指定事项
        self.remove(event)
        # 并将它添加到已完成事项列表中
        self.client.lpush(self.done_list, event)

    def show_todo_list(self):
        """
        列出所有待办事项。
        """
        return self.client.lrange(self.todo_list, 0, -1)

    def show_done_list(self):
        """
        列出所有已完成事项。
        """
        return self.client.lrange(self.done_list, 0, -1)
