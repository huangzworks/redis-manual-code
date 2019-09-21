def make_action_key(action):
    return "action_recorder::" + action

class ActionRecorder:

    def __init__(self, client, action):
        self.client = client
        self.bitmap = make_action_key(action)

    def perform_by(self, user_id):
        """
        记录执行了指定行为的用户。
        """
        self.client.setbit(self.bitmap, user_id, 1)

    def is_performed_by(self, user_id):
        """
        检查给定用户是否执行了指定行为，是的话返回 True ，反之返回 False 。
        """
        return self.client.getbit(self.bitmap, user_id) == 1

    def count_performed(self):
        """
        返回执行了指定行为的用户人数。
        """ 
        return self.client.bitcount(self.bitmap)
