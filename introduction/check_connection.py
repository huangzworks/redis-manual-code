from redis import Redis

client = Redis()

# ping() 方法在连接正常时将返回 True
if client.ping() is True:
    print("connecting")
else:
    print("disconnected")
