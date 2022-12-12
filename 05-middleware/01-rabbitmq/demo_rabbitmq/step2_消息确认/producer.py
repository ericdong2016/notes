#!/usr/bin/env python
import pika

# 链接rabbit服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

# 创建频道
channel = connection.channel()

# 创建一个队列名叫hello
channel.queue_declare(queue='hello')

# 向队列插入数值 routing_key是队列名 body是要插入的内容
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=b'Hello World!')
print("开始队列")
connection.close()
