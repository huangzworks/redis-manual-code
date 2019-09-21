#coding:utf-8

from redis import Redis
from db_sampler import DbSampler
from create_random_type_keys import create_random_type_keys

r = Redis()

r.flushdb()

create_random_type_keys(r, 1000)

s = DbSampler(r)

s.sample()
