https://www.rabbitmq.com/dlx.html

https://www.freesion.com/article/5217425389/



DLX，全称为Dead-Letter-Exchange , 可以称之为死信交换机，也有人称之为死信邮箱。当消息在一个队列中变成死信(dead message)之后，它能被重新发送到另一个交换机中，这个交换机就是DLX ，绑定DLX的队列就称之为死信队列。

消息变成死信，可能是由于以下的原因：

消息被拒绝
消息过期
队列达到最大长度
DLX也是一个正常的交换机，和一般的交换机没有区别，它能在任何的队列上被指定，实际上就是设置某一个队列的属性。当这个队列中存在死信时，Rabbitmq就会自动地将这个消息重新发布到设置的DLX上去，进而被路由到另一个队列，即死信队列。

要想使用死信队列，只需要在定义队列的时候设置队列参数 x-dead-letter-exchange 指定交换机即可。

# 指定最长时间
channel.queue_declare(queue='task_queue', durable=True, arguments={"x-message-ttl": 10000, "x-dead-letter-exchange": 'task_queue_dead'})
# 指定最长长度
channel.queue_declare(queue='task_queue', durable=True, arguments={"x-max-length": 200, "x-dead-letter-exchange": 'task_queue_dead'})

# 指定route-key
x-dead-letter-routing-key


