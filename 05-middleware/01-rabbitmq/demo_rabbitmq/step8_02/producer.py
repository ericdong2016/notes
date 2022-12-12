from demo_rabbitmq.step8_02.client import RabbitMQClient

print("start program")
client = RabbitMQClient()
msg1 = '{"key":"value"}'
client.publish_message('test.py-delay',msg1, delay=1,TTL=10000)
print("message send out")

# 要测试死信队列，不需要启动consumer
