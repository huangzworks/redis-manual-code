local result_key = KEYS[1]

local aggregate_work = function()
    -- ... 省略大量代码
end

redis.call('SET', result_key, aggregate_work())
