#!/usr/bin/env python
import pika

# ######################### 生产者 #########################
# 连接rabbit服务器（localhost是本机，如果是其他服务器请修改为ip地址）
# 可在后面添加端口， vhost等
# 添加用户名和密码 pika.PlainCredentials   https://www.cnblogs.com/cwp-bg/p/8426188.html
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

# 创建频道
channel = connection.channel()

# 创建一个队列名叫hello
# 声明（创建）队列
"""
*参数1：队列名称
*参数2: 
*参数3：是否定义持久化队列
*参数4：是否独占本次连接
*参数5：是否在不使用的时候自动删除队列, 设置为true, 则在producer, cosumer都推出后，该queue会自动删除掉
*参数6：队列其它参数
"""
channel.queue_declare(queue='hello')

"""
exchange -- 它使我们能够确切地指定消息应该到哪个队列去。
routing_key -- 队列名
body -- 要插入的内容
mandatory --  当mandatory标志位设置为true时，如果exchange根据自身类型和消息routingKey无法找到一个合适的queue存储消息，
那么broker会调用basic.return方法将消息返还给生产者;当mandatory设置为false时，出现上述情况broker会直接将消息丢弃;通俗的讲，
mandatory标志告诉broker代理服务器至少将消息route到一个队列中，否则就将消息return给发送者;

"""

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=b'Hello World!')

print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
channel.close()
connection.close()

