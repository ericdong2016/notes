#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

channel = connection.channel()

# 设置死信队列
channel.exchange_declare(exchange='RetryExchange',
                              exchange_type='fanout',
                              durable=True)

channel.queue_declare(queue='RetryQueue',
                           durable=True)
channel.queue_bind('RetryQueue', 'RetryExchange', 'RetryQueue')

# 设置过期队列
# channel.queue_declare(queue='task_queue1', durable=True, arguments={"x-message-ttl": 10000, "x-dead-letter-exchange": 'task_queue_dead'})


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    import time
    time.sleep(5)
    print('ok')

    ch.basic_ack(delivery_tag=method.delivery_tag)



# 设置过期队列
queue_name = "RetryQueue"
channel.queue_declare(queue=queue_name,durable=True, )

# 表示谁来谁取，不再按照奇偶数排列
# 消息未处理完前不要发送信息的消息
channel.basic_qos(prefetch_count=1)


# channel.basic_consume(on_message_callback=callback,
#                       queue=queue_name,
#                       auto_ack=False)

channel.basic_consume(on_message_callback=callback,
                      queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
