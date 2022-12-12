延迟队列 = ttl + 死信队列

step8已经实现

或者
https://www.rabbitmq.com/lazy-queues.html

args.put("x-queue-mode", "lazy");



一些常见参数：
    https://www.cnblogs.com/hello-/articles/10339602.html

    Message TTL消息剩余生存时间
    为该队列的所有消息统一设置相同的声明周期：统一设置队列中的所有消息的过期时间，例如设置10秒，10秒后这个队列的消息清零

    arguments.put("x-message-ttl", 10000);

    // 声明队列时指定队列中的消息过期时间
    channel.queue_declare(QUEUE_NAME, false, false, false, arguments);
    Auto Expire自动过期
    x-expires用于当多长时间没有消费者访问该队列的时候，该队列会自动删除，可以设置一个延迟时间，如仅启动一个生产者，10秒之后该队列会删除，或者启动一个生产者，再启动一个消费者，消费者运行结束后10秒，队列也会被删除

    Max Length最大长度
    x-max-length:用于指定队列的长度，如果不指定，可以认为是无限长，例如指定队列的长度是4，当超过4条消息，前面的消息将被删除，给后面的消息腾位

    Max Length Bytes代码片段
    x-max-length-bytes: 用于指定队列存储消息的占用空间大小，当达到最大值是会删除之前的数据腾出空间

    Maximum priority最大优先级
    x-max-priority: 设置消息的优先级，优先级值越大，越被提前消费。


