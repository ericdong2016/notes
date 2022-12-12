import pika

# 链接rabbit
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))
# 创建频道
channel = connection.channel()
# 如果生产者没有运行创建队列，那么消费者创建队列
channel.exchange_declare(exchange="topic", exchange_type="topic")

# 查看官网的文档，queue="", 可生成一个随机的队列名
result = channel.queue_declare(queue="", exclusive=True)
q_name = result.method.queue

severities = sys.argv[1:]

if severities:
    for severity in severities:
        channel.queue_bind(exchange="topic", queue=q_name, routing_key=severity)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print('ok')


channel.basic_consume(on_message_callback=callback,
                      queue=q_name,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

import time
time.sleep(10)
