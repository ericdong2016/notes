# from oslo_config import cfg
# import oslo_messaging  as messaging
#
#
# def rpc_client(func_name, **kwargs):
#     transport = messaging.get_transport(cfg.CONF, url="rabbit://guest:guest@192.168.19.160:5672/")
#     target = messaging.Target(topic='test_topic')
#     client = messaging.RPCClient(transport, target)
#     print("func_name:", func_name)
#     print("kwargs:", kwargs)
#     ret = client.call(ctxt={}, method=func_name, kwargs=kwargs)
#     cctx = client.prepare(namespace='control',version='1.0')
#     cctx.cast({}, 'stop')
#     return ret

from flask import g


def rpc_client(func_name, **kwargs):
    client = g.client
    result = client.call(ctxt={}, method=func_name, kwargs=kwargs)
    cctx = client.prepare(namespace='control', version='1.0')
    cctx.cast({}, 'stop')
    return result
