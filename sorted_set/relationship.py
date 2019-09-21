#coding:utf-8

from time import time
from timeline import Timeline

def following_key(user):
    return user + "::following"

def follower_key(user):
    return user + "::follower"


class Relationship:

    def __init__(self, client, user):
        self.client = client
        self.user = user

    def follow(self, target):
        current_time = time()

        user_following_tl = Timeline(self.client, following_key(self.user))
        user_following_tl.add(target, current_time)

        target_follower_tl = Timeline(self.client, follower_key(target))
        target_follower_tl.add(self.user, current_time)

    def unfollow(self, target):
        user_following_tl = Timeline(self.client, following_key(self.user))
        user_following_tl.remove(target)
        target_follower_tl = Timeline(self.client, follower_key(target))
        target_follower_tl.remove(self.user)
