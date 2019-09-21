def mlpop(client, list_key, number):
    # 开启事务
    transaction = client.pipeline()
    # 将多个 LPOP 命令放入事务队列
    for i in range(number):
        transaction.lpop(list_key)
    # 执行事务
    return transaction.execute()
