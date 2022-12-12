from flask import Flask, jsonify, g
from oslo_config import cfg
from demo_rabbitmq.step11_oslo_messeging.client import rpc_client
import oslo_messaging  as messaging
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename="./client.log", filemode="a")

app = Flask(__name__)

transport = messaging.get_transport(cfg.CONF, url="rabbit://admin:admin123@192.168.19.160:5672/")
target = messaging.Target(topic='test_topic')
client = messaging.RPCClient(transport, target, timeout=40000)


@app.before_request
def before_request():
    g.client = client


@app.route("/")
def index():
    result = rpc_client(func_name='index', hello="client test.py")
    logging.info("client result:")
    return jsonify(status=200, data=result)


if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
