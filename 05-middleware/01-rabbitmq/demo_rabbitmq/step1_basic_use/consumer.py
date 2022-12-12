#!/usr/bin/env python
import pika

# ########################## 消费者 ##########################
# 链接rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160', ))

# 创建频道
channel = connection.channel()

# 如果生产者没有运行创建队列，那么消费者也许就找不到队列了。为了避免这个问题
# 所有消费者也创建这个队列
channel.queue_declare(queue='hello')


# 接收消息需要使用callback这个函数来接收，他会被pika库来调用
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# 从队列取数据 callback是回调函数 如果拿到数据 那么将执行callback函数
channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True)

print(' [*] 等待信息. To exit press CTRL+C')
# 永远循环等待数据处理和callback处理的数据
channel.start_consuming()
channel.close()
