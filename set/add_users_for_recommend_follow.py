from redis import Redis
from relationship import Relationship
from recommend_follow import RecommendFollow

client = Redis()

# user
peter = Relationship(client, "peter")

# targets
jack = Relationship(client, "jack")
tom = Relationship(client, "tom")
mary = Relationship(client, "mary")
david = Relationship(client, "david")
sam = Relationship(client, "sam")

# user follow targets
peter.follow("jack")
peter.follow("tom")
peter.follow("mary")
peter.follow("david")
peter.follow("sam")

for i in range(10):
    jack.follow("J{0}".format(i))
    tom.follow("T{0}".format(i))
    mary.follow("M{0}".format(i))
    david.follow("D{0}".format(i))
    sam.follow("S{0}".format(i))
