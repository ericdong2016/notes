import pika

# 链接rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

# 创建频道
channel = connection.channel()

# 如果生产者没有运行创建队列，那么消费者创建队列
# 1. 如果想让队列实现持久化那么加上durable=True
channel.queue_declare(queue='hello1', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    import time
    time.sleep(10)
    print('ok')

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 主要使用此代码


# auto_ack=False 需要设置为手动确认，原因是：自动确认会在消息发送给消费者，消费者在消费过程出现异常，这样存在丢失消息的可能。
channel.basic_consume(on_message_callback=callback,
                      queue='hello1',
                      auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
