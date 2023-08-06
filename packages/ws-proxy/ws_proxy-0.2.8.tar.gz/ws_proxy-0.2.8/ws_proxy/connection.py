# coding: utf8

import gevent
from netkit.contrib.tcp_client import TcpClient
from .utils import safe_func, safe_call
from .log import logger


class Connection(object):

    environ = None

    server = None

    proxy_client = None
    backend_client = None

    def __init__(self, server):
        super(Connection, self).__init__()
        self.server = server

    def handle(self, environ, start_response):
        self.environ = environ
        self.proxy_client = self.environ["wsgi.websocket"]
        if not self.proxy_client:
            # 说明不是websocket
            return

        self.backend_client = TcpClient(self.server.config.BOX_CLASS, address=self.server.config.BACKEND_ADDR)
        try:
            self.backend_client.connect()
        except:
            logger.error('exc occur.', exc_info=True)
            self.close()
            return

        jobs = []

        for func in [self.recv_from_ws, self.recv_from_gw]:

            jobs.append(gevent.spawn(func))

        gevent.joinall(jobs)

        self.close()

    def recv_from_ws(self):
        while not self.closed():
            def inner_handle():
                try:
                    message = self.proxy_client.receive()
                    if not message:
                        self.close()
                        return
                    # 必须转化格式，原来是bytearray
                    message = bytes(message)
                except:
                    logger.error('exc occur.', exc_info=True)
                    self.close()
                    return

                try:
                    self.backend_client.write(message)
                except:
                    logger.error('exc occur.', exc_info=True)
                    self.close()
                    return

            gevent.spawn(safe_func(inner_handle)).join()

    def recv_from_gw(self):
        while not self.closed():
            def inner_handle():
                try:
                    box = self.backend_client.read()
                    if not box:
                        self.close()
                        return
                except:
                    logger.error('exc occur.', exc_info=True)
                    self.close()
                    return

                message = box.pack()

                try:
                    self.proxy_client.send(message, binary=True)
                except:
                    logger.error('exc occur.', exc_info=True)
                    self.close()
                    return

            gevent.spawn(safe_func(inner_handle)).join()

    def close(self):
        if self.proxy_client:
            try:
                self.proxy_client.close()
            except:
                logger.error('exc occur.', exc_info=True)
            finally:
                self.proxy_client = None

        if self.backend_client:
            try:
                self.backend_client.close()
            except:
                logger.error('exc occur.', exc_info=True)
            finally:
                self.backend_client = None

    def closed(self):
        return not self.proxy_client or not self.proxy_client
