class Cache:

    def __init__(self, client):
        self.client = client

    def set(self, key, value):
        """
        把需要被缓存的数据储存到键 key 里面，
        如果键 key 已经有值，那么使用新值去覆盖旧值。
        """
        self.client.set(key, value)

    def get(self, key):
        """
        获取储存在键 key 里面的缓存数据，
        如果数据不存在，那么返回 None 。
        """
        return self.client.get(key)

    def update(self, key, new_value):
        """
        对键 key 储存的缓存数据进行更新，
        并返回键 key 在被更新之前储存的缓存数据。
        如果键 key 之前并没有储存数据，
        那么返回 None 。
        """
        return self.client.getset(key, new_value)
