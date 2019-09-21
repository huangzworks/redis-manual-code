#coding:utf-8

from action_recorder import make_action_key

class ActionAggregation:

    def __init__(self, client):
        self.client = client

    def calc_and(self, result_action, *input_actions):
        """
        对给定的用户行为记录执行并计算。
        """
        action_keys = map(make_action_key, input_actions)
        result_key = make_action_key(result_action)
        self.client.bitop("AND", result_key, *action_keys)

    def calc_or(self, result_action, *input_actions):
        """
        对给定的用户行为记录执行或计算。
        """
        action_keys = map(make_action_key, input_actions)
        result_key = make_action_key(result_action)
        self.client.bitop("OR", result_key, *action_keys)
      
    def calc_xor(self, result_action, *input_actions):
        """
        对给定的用户行为记录执行异或计算。
        """
        action_keys = map(make_action_key, input_actions)
        result_key = make_action_key(result_action)
        self.client.bitop("XOR", result_key, *action_keys)
       
    def calc_not(self, result_action, input_action):
        """
        对给定的用户行为记录执行非计算。
        """
        action_key = make_action_key(input_action)
        result_key = make_action_key(result_action)
        self.client.bitop("NOT", result_key, action_key)
