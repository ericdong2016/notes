#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/8/27 21:16 
# @Author : donghuan 
# @File : rpc_client.py 
# @Software: PyCharm


# !/usr/bin/env python
# import pika
# import uuid
#
#
# class FibonacciRpcClient(object):
#     def __init__(self):
#         self.connection = pika.BlockingConnection(pika.ConnectionParameters(
#             host='192.168.65.128'))
#
#         self.channel = self.connection.channel()
#
#         result = self.channel.queue_declare(queue="", exclusive=True)
#         self.callback_queue = result.method.queue
#
#         # 接受server发送的消息
#         self.channel.basic_consume(on_message_callback=self.on_response,
#                                    queue=self.callback_queue, auto_ack=True, )
#
#     def on_response(self, ch, method, props, body):
#         if self.corr_id == props.correlation_id:
#             self.response = body
#
#     def call(self, n):
#         self.response = None
#         self.corr_id = str(uuid.uuid4())
#
#         # 往server发送消息
#         self.channel.basic_publish(exchange='', routing_key='rpc_queue',
#                                    properties=pika.BasicProperties(
#                                        reply_to=self.callback_queue,
#                                        correlation_id=self.corr_id,
#                                    ),
#                                    body= str(n))
#
#         while self.response is None:
#             # 检查队列里有没有消息，不会阻塞
#             self.connection.process_data_events()
#         return int(self.response)
#
#
# fibonacci_rpc = FibonacciRpcClient()
# print(" [x] Requesting fib(30)")
#
# response = fibonacci_rpc.call(30)
# print(" [.] Got %r" % response)


import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.19.160'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()
print(" computing...")
response = fibonacci_rpc.call(10)
print(" Got server result: %r" % response)
