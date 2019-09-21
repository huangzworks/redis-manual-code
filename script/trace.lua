local f1 = function()
    local f2 = function()
        local f3 = function()
            redis.breakpoint()
        end
        f3()
    end
    f2()
end

f1()
