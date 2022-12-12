#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True, arguments={"x-message-ttl": 10000, "x-dead-letter-exchange": 'task_queue_dead'})  # 设置队列持久化


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    import time
    time.sleep(10)
    print('ok')

    ch.basic_ack(delivery_tag=method.delivery_tag)


# 表示谁来谁取，不再按照奇偶数排列
channel.basic_qos(prefetch_count=1)      # 消息未处理完前不要发送信息的消息

channel.basic_consume(on_message_callback=callback,
                      queue='task_queue',
                      auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
