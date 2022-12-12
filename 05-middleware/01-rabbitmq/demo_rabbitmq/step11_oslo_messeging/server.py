import logging
import time

import oslo_messaging
from oslo_config import cfg

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename="./server.log", filemode="a")


class ServerControlEndpoint(object):
    target = oslo_messaging.Target(namespace='control')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if self.server:
            self.server.stop()


class BasicEndpoint(object):
    def index(self, ctx, kwargs):
        print("ctx:", ctx)
        print("kwargs:", kwargs)
        logging.info("******************************")
        logging.info(kwargs)
        logging.info("******************************")
        return "server response"


transport = oslo_messaging.get_transport(cfg.CONF, url="rabbit://admin:admin123@192.168.19.160:5672/")
target = oslo_messaging.Target(topic='test_topic', server="test_server", namespace='control', version='1.0')
endpoints = [
    ServerControlEndpoint(None),
    BasicEndpoint()
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='threading')
try:
    server.start()
    logging.info("startting server")
    while True:
        time.sleep(1)
except Exception as e:
    logging.info("Stopping server")
    print(e)

server.stop()
server.wait()
