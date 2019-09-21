#coding:utf-8

from redis import Redis
from density_map import DensityMap

r = Redis()
r.flushdb()

map = DensityMap(r, 'a-density-map')

content = [['1', '0', '1'], ['0', '1', '1'], ['1', '0', '0']]

#

map.set_row(0, *content[0])
map.set_row(1, *content[1])
map.set_row(2, *content[2])

assert(
    map.get_row(0) == content[0]
)
assert(
    map.get_row(1) == content[1]
)
assert(
    map.get_row(2) == content[2]
)

#

assert(
    map.get_value(0, 0) == '1'
)

map.set_value(0, 0, '0')

assert(
    map.get_value(0, 0) == '0'
)

#

r.flushdb()

map.set_map(content)

assert(
    map.get_map(len(content)) == content
)

#

r.flushdb()

print("All tests passed!")
