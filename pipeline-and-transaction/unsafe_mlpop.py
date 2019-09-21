def mlpop(client, list_key, number):
    # 用于储存被弹出元素的结果列表
    items = []  
    for i in range(number):
        # 执行 LPOP 命令，弹出一个元素
        poped_item = client.lpop(list_key)
        # 将被弹出的元素追加到结果列表末尾
        items.append(poped_item)
    # 返回结果列表
    return items
