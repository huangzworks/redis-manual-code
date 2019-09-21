class VolatileCache:

    def __init__(self, client):
        self.client = client

    def set(self, key, value, timeout):
        """
        把数据缓存到键 key 里面，并为其设置过期时间。
        如果键 key 已经有值，那么使用新值去覆盖旧值。
        """
        self.client.set(key, value, ex=timeout)

    def get(self, key):
        """
        获取键 key 储存的缓存数据。
        如果键不存在，又或者缓存已经过期，那么返回 None 。
        """
        return self.client.get(key)
