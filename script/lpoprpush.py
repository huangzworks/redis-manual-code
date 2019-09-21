def lpoprpush(client, source, target):
    script = """
    local source = KEYS[1]
    local target = KEYS[2]

    -- 从源列表左端弹出一个元素
    -- 当源列表为空时，LPOP 返回的 nil 将被 Lua 转换为 false
    local item = redis.call("LPOP", source)

    -- 如果被弹出元素不为空，那么将它推入到目标列表的右端
    -- 并向调用者返回该元素
    if item ~= false then
        redis.call("RPUSH", target, item)
        return item
    end
    """
    return client.eval(script, 2, source, target)
