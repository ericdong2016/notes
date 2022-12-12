#!/usr/bin/env python
import pika

# 链接rabbit服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))
# 创建频道
channel = connection.channel()

channel.exchange_declare(exchange='fanout', exchange_type="fanout")

# 因为是广播，索引不需要指定routing_key
channel.basic_publish(exchange='fanout',
                      routing_key='',
                      body=b'Hello World!',
                      # properties=pika.BasicProperties(
                      #     delivery_mode=2,
                      #     # 标记我们的消息为持久化的 - 通过设置 delivery_mode 属性为 2
                      #     # 这样必须设置，让消息实现持久化
                      # )
                      )
# 这个exchange参数就是这个exchange的名字. 空字符串标识默认的或者匿名的exchange：如果存在routing_key, 消息路由到routing_key指定的队列中。
print(" [x] 开始队列'")
connection.close()
