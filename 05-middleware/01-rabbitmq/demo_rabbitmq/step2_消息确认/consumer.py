#!/usr/bin/env python
import pika

# http://rabbitmq.mr-ping.com/tutorials_with_python/[2]Work_Queues.html

# 链接rabbit服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

# 创建频道
channel = connection.channel()

# 如果生产者没有运行创建队列，那么消费者创建队列
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    """
     - channel: BlockingChannel
     - method: spec.Basic.Deliver
     - properties: spec.BasicProperties
     - body: bytes

    """
    print(" [x] Received %r" % body)

    import time
    time.sleep(10)
    print("method.delivery_tag:", method.delivery_tag)  # method.delivery_tag  1，2，3, 仅仅是一个传递标识

    # 2. 主要使用此代码，手动应答
    ch.basic_ack(delivery_tag=method.delivery_tag)      # 主要使用此代码


# 1. auto_ack=False 需要设置为手动确认，  原因是：自动确认会在消息发送给消费者，消费者在消费过程出现异常，这样存在丢失消息的可能。
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=False)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
