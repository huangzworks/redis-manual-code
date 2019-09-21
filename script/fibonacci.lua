local n = tonumber(ARGV[1])

-- F(0) = 0 , F(1) = 1
local i = 0
local j = 1

-- F(n) = F(n-1)+F(n-2)
while n ~= 0 do
    i, j = j, i+j
    n = n-1
    redis.debug(i)
end

return i
