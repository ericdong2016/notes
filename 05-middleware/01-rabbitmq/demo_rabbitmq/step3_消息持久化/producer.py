#!/usr/bin/env python
import pika

# 链接rabbit服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))
# 创建频道
channel = connection.channel()

# 1. 如果想让队列实现持久化那么加上durable=True
channel.queue_declare(queue='hello1', durable=True)


# 这个exchange参数就是这个exchange的名字. 空字符串标识默认的或者匿名的exchange：如果存在routing_key, 消息路由到routing_key指定的队列中。
# 2. 标记我们的消息为持久化的 - 通过设置 delivery_mode 属性为 2
channel.basic_publish(exchange='',
                      routing_key='hello1',
                      body=b'Hello World!',
                      properties=pika.BasicProperties(delivery_mode=2, ))


print(" [x] 开始队列'")
connection.close()
