import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

channel = connection.channel()

# 设置队列为持久化的队列
channel.queue_declare(queue='task_queue', durable=True)

message = b' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,     # 设置消息为持久化的
                      ))
print(" [x] Sent %r" % message)
connection.close()
