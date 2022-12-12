import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

channel = connection.channel()

#  设置死信交换机和队列，以及绑定
channel.exchange_declare(exchange='RetryExchange',
                              exchange_type='fanout',
                              durable=True)

channel.queue_declare(queue='RetryQueue',
                           durable=True)
channel.queue_bind('RetryQueue', 'RetryExchange', 'RetryQueue')


# channel.queue_declare(queue='task_queue1',
#                       durable=True,
#                       arguments={"x-message-ttl": 10000, "x-dead-letter-exchange": 'task_queue_dead'})

message = b' '.join(sys.argv[1:]) or "Hello World!"


# 设置过期队列
arguments = {}
# 设置死信转发的exchange
arguments['x-dead-letter-exchange'] = "RetryExchange"
arguments['x-message-ttl'] = 10000

channel.queue_declare(queue="test_queue1",
                           durable=True,
                           arguments=arguments)


# 发布
channel.basic_publish(exchange='',
                      routing_key='test_queue1',
                      body=message,
                      # 设置消息为持久化的
                      properties=pika.BasicProperties(delivery_mode=2, ))

print(" [x] Sent %r" % message)
connection.close()
