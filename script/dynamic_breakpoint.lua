local i = 1
local target = tonumber(ARGV[1])
while true do
    if i > target then
        redis.breakpoint()
        return "bye bye"
    end
    i = i+1
end
