from demo_rabbitmq.step8_02.client import RabbitMQClient

print("start program")
client = RabbitMQClient()


def callback(ch, method, properties, body):
    msg = body.decode()
    print(msg)
    # 如果处理成功，则调用此消息回复ack，表示消息成功处理完成。
    RabbitMQClient.message_handle_successfully(ch, method)


queue_name = "RetryQueue"
client.start_consume(callback, queue=queue_name, delay=0)
