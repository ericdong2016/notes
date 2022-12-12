import pika

# 链接rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

# 创建频道
channel = connection.channel()

# 指定exchange
channel.exchange_declare(exchange="fanout", exchange_type="fanout")

# 如果生产者没有运行创建队列，那么消费者创建队列
# 查看官网的文档，queue="", 可生成一个随机的队列名
# 这时候我们可以通过result.method.queue获得已经生成的随机队列名。它可能是这样子的：amq.gen-U0srCoW8TsaXjNh73pnVAw==。
# 当与消费者（consumer）断开连接的时候，这个队列应当被立即删除。exclusive标识符即可达到此目的。

result = channel.queue_declare(queue="", exclusive=True)

# 拿到随机的队列名
q_name = result.method.queue

# 绑定queue， 因为是广播，所以不指定routing_key
channel.queue_bind(exchange="fanout", queue=q_name)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print('ok')


# 开启了自动应答
channel.basic_consume(on_message_callback=callback,
                      queue=q_name,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
import time

time.sleep(10)
