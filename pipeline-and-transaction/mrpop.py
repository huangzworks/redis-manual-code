#coding:utf-8

def mrpop(client, list_key, number):
    # 开启事务
    transaction = client.pipeline()
    # 将多个 RPOP 命令放入到事务队列里面
    for i in range(number):
        transaction.rpop(list_key)
    # 执行事务
    return transaction.execute()
