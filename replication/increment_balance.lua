local user_balance_keys = KEYS
local increment = ARGV[1]

-- 遍历所有给定的用户余额键，对它们执行 INCRBY 操作
for i = 1, #user_balance_keys do
    redis.call('INCRBY', user_balance_keys[i], increment)
end
