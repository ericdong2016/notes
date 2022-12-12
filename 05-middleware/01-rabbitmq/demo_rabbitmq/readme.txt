
参考文档：
https://www.cnblogs.com/liu-yao/p/5678161.html

https://www.cnblogs.com/alex3714/articles/5248247.html

http://rabbitmq.mr-ping.com/tutorials_with_python/[1]Hello_World.html      包括python /go 代码


机器： 192.168.19.160


常规安装：
安装配置epel源
   $ rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

安装erlang
   $ yum -y install erlang

安装RabbitMQ
   $ yum -y install rabbitmq-server


service rabbitmq-server start/stop



容器化安装：
docker run -d --hostname my-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3.8.0-beta.4-management

docker-compose.yaml


代码：
pip install pika==1.1



常用指令：
rabbitmqctl list_queues
rabbitmqctl list_exchanges
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app

rabbitmqctl list_bindings 列出所有现存的绑定。





step1 基本使用

step2 work queue 之 消息确认

    可实现依次分发(开启两个consumer), 负载均衡， 消息不丢失(消息确认, auto_ack = false 或者no_ack=true 移除)

    bug：
        pika.exceptions.ChannelClosedByBroker: (406, 'PRECONDITION_FAILED - unknown delivery tag 1')

        auto_ack=False

    消息确认：
        为了防止消息丢失，RabbitMQ提供了消息响应（acknowledgments）。消费者会通过一个ack（响应），告诉RabbitMQ已经收到并处理了某条消息，然后RabbitMQ就会释放并删除这条消息。

        如果消费者（consumer）挂掉了，没有发送响应，RabbitMQ就会认为消息没有被完全处理，然后重新发送给其他消费者（consumer）。这样，即使工作者（workers）偶尔的挂掉，也不会丢失消息。


    忘记确认：
        一个很容易犯的错误就是忘了basic_ack，后果很严重。消息在你的程序退出之后就会重新发送，如果它不能够释放没响应的消息，RabbitMQ就会占用越来越多的内存。

        为了排除这种错误，你可以使用rabbitmqctl命令，输出messages_unacknowledged字段：

        $ sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
        Listing queues ...
        hello    0       0
        ...done.




step3  work queue 之 消息持久化
    bug
        pika.exceptions.ChannelClosedByBroker: (406, "PRECONDITION_FAILED - parameters for queue 'hello' in vhost '/' not equivalent")

        更改生产者，消费者名字


    所谓的消息持久化指的是，consumer获取道producer的消息后，即便中间出现问题(比如断开连接)，重新连接上去后依然继续能应答

    注意：
        将消息设为持久化并不能完全保证不会丢失。以上代码只是告诉了RabbitMq要把消息存到硬盘，但从RabbitMq收到消息到保存之间还是有一个很小的间隔时间。因为RabbitMq并不是所有的消息都使用fsync(2)——它有可能只是保存到缓存中，并不一定会写到硬盘中。并不能保证真正的持久化，但已经足够应付我们的简单工作队列。如果你一定要保证持久化，你需要改写你的代码来支持事务（transaction）。


step4 work queue 之 消息顺序(公平调度)

    channel.basic_qos(prefetch_count=1)



step5 发布订阅(有四种方式)
    发布订阅(step5)和简单的消息队列（step1-step4）区别:
        发布订阅会将消息发送给所有的订阅者， 而消息队列中的数据被消费一次便消失。
        所以RabbitMQ实现发布和订阅时，会为每一个订阅者创建一个队列， 而发布者发布消息时，会将消息放置在所有相关队列中。



step6 rpc
    rpc_queue 队列中有数据导致一直无法运行  可以手动删除queue


step7  ttl

step8  dlx

step9  lazy queue


其他常见问题：
    1. 消息积压
        当消息生产的速度长时间，远远大于消费的速度时。就会造成消息堆积。

        消息堆积的影响

            可能导致新消息无法进入队列
            可能导致旧消息无法丢失
            消息等待消费的时间过长，超出了业务容忍范围。

        产生堆积的情况
            生产者突然大量发布消息
            消费者消费失败
            消费者出现性能瓶颈。
            消费者挂掉

        解决办法
            排查消费者的消费性能瓶颈
            增加消费者的多线程处理
            部署增加多个消费者


        场景重现：让消息产生堆积

            生产者大量发送消息：使用Jmeter开启多线程，循环发送消息大量进入队列。 模拟堆积10万条数据

            消费者消费失败：随机抛出异常，模拟消费者消费失败，没有ack（手动ack的时候）。

            设置消费者的性能瓶颈：在消费方法中设置休眠时间，模拟性能瓶颈

            关闭消费者：停掉消费者，模拟消费者挂掉


        问题解决：消息已经堆积如何解决
            消息队列堆积，想办法把消息转移到一个新的队列，增加服务器慢慢来消费这个消息可以

            1、解决消费者消费异常问题

            2、解决消费者的性能瓶颈：改短休眠时间

            3、增加消费线程，增加多台服务器部署消费者。快速消费。



    2. 消息丢失，消息补偿
        在实际的生产环境中有可能出现一条消息因为一些原因丢失，导致消息没有消费成功，从而造成数据不一致等问题，造成严重的影响，
        比如：在一个商城的下单业务中，需要生成订单信息和扣减库存两个动作，如果使用RabbitMQ来实现该业务，
        那么在订单服务下单成功后需要发送一条消息到库存服务进行扣减库存，如果在此过程中，一条消息因为某些原因丢失，
        那么就会出现下单成功但是库存没有扣减，从而导致超卖的情况，也就是库存已经没有了，但是用户还能下单，这个问题对于商城系统来说是致命的。

        消息丢失的场景主要分为：1.消息在生产者丢失，2.消息在RabbitMQ丢失，3.消息在消费者丢失。

        2.1 消息在生产者丢失
            场景介绍
                消息生产者发送消息成功，但是MQ没有收到该消息，消息在从生产者传输到MQ的过程中丢失，一般是由于网络不稳定的原因。

            解决方案
                采用RabbitMQ 发送方消息确认机制，当消息成功被MQ接收到时，会给生产者发送一个确认消息，表示接收成功。
                RabbitMQ 发送方消息确认模式有以下三种：普通确认模式，批量确认模式，异步监听确认模式。spring整合RabbitMQ后只使用了异步监听确认模式。

                publisher-confirms="true"

                说明:异步监听模式，可以实现边发送消息边进行确认，不影响主线程任务执行。


        2.2 消息在RabbitMQ丢失
            场景介绍
                消息成功发送到MQ，消息还没被消费却在MQ中丢失，比如MQ服务器宕机或者重启会出现这种情况

            解决方案
                持久化交换机，队列，消息，确保MQ服务器重启时依然能从磁盘恢复对应的交换机，队列和消息。

                spring整合后默认开启了交换机，队列，消息的持久化，所以不修改任何设置就可以保证消息不在RabbitMQ丢失。但是为了以防万一，还是可以申明下。


        2.3 消息在消费者丢失
            场景介绍
                消息费者消费消息时，如果设置为自动回复MQ，消息者端收到消息后会自动回复MQ服务器，MQ则会删除该条消息，
                如果消息已经在MQ被删除但是消费者的业务处理出现异常或者消费者服务宕机，那么就会导致该消息没有处理成功从而导致该条消息丢失。

            解决方案
                设置为手动回复MQ服务器，当消费者出现异常或者服务宕机时，MQ服务器不会删除该消息，而是会把消息重发给绑定该队列的消费者，如果该队列只绑定了一个消费者，那么该消息会一直保存在MQ服务器，直到消息者能正常消费为止。
                本解决方案以一个队列绑定多个消费者为例来说明，一般在生产环境上也会让一个队列绑定多个消费者也就是工作队列模式来减轻压力，提高消息处理效率

            MQ重发消息场景：
                1.消费者未响应ACK，主动关闭频道或者连接
                2.消费者未响应ACK，消费者服务挂掉
                3.消息重复，消息幂等

    3. 有序消费
        场景介绍
            场景1
                当RabbitMQ采用work Queue模式，此时只会有一个Queue但是会有多个Consumer,同时多个Consumer直接是竞争关系，此时就会出现MQ消息乱序的问题。

             解决1
                根据id算hash， 然后对队列个数取余， 就可以让相同id的所有操作压到同一个队列，且一个队列只有一个消费者，就不会乱序

            场景2
                当RabbitMQ采用简单队列模式的时候,如果消费者采用多线程的方式来加速消息的处理,此时也会出现消息乱序的问题。

            解决2
                消费者拉取消息后，根据id算hash， 然后对队列个数取余， 就可以让相同id的所有操作压到同一个队列，让同一个线程去处理，就不会乱序




    4. 重复消费(消费幂等)
        场景介绍
            为了防止消息在消费者端丢失，会采用手动回复MQ的方式来解决，同时也引出了一个问题，消费者处理消息成功，
            手动回复MQ时由于网络不稳定，连接断开，导致MQ没有收到消费者回复的消息，那么该条消息还会保存在MQ的消息队列，
            由于MQ的消息重发机制，会重新把该条消息发给和该队列绑定的消息者处理，这样就会导致消息重复消费。
            而有些操作是不允许重复消费的，比如下单，减库存，扣款等操作。

            MQ重发消息场景：

            1.消费者未响应ACK，主动关闭频道或者连接

            2.消费者未响应ACK，消费者服务挂掉


        解决方案
            如果消费消息的业务是幂等性操作（同一个操作执行多次，结果不变）就算重复消费也没问题，可以不做处理，如果不支持幂等性操作，如：下单，减库存，扣款等，
            那么可以在消费者端每次消费成功后将该条消息id保存到数据库，每次消费前查询该消息id，如果该条消息id已经存在那么表示已经消费过就不再消费否则就消费。
            本方案采用redis存储消息id，因为redis是单线程的，并且性能也非常好，提供了很多原子性的命令，本方案使用setnx命令存储消息id。

            setnx(key,value):如果key不存在则插入成功且返回1, 如果key存在,则不进行任何操作,返回0



