
https://www.rabbitmq.com/ttl.html


过期时间TTL表示可以对消息设置预期的时间，在这个时间内都可以被消费者接收获取；过了之后消息将自动被删除。RabbitMQ可以对消息和队列设置TTL。目前有两种方法可以设置。

第一种方法是通过队列属性设置，队列中所有消息都有相同的过期时间。
    channel.queue_declare(queue='task_queue', durable=True, arguments={"x-message-ttl": 1000})

第二种方法是对消息进行单独设置，每条消息TTL可以不同。

    channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,                  # 设置消息为持久化的
                          expiration= 1000                  # 给单条消息设置ttl
                      ))


如果上述两种方法同时使用，则消息的过期时间以两者之间TTL较小的那个数值为准。消息在队列的生存时间一旦超过设置的TTL值，
就称为dead message被投递到死信队列， 消费者将无法再收到该消息。
