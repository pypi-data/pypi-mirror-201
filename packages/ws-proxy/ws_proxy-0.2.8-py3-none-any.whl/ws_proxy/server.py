# coding: utf8

import ssl
import logging.config
from geventwebsocket.server import WebSocketServer

from .connection import Connection


class Server(object):

    connection_class = Connection

    # BOX_CLASS = None
    # PROXY_ADDR = None
    # BACKEND_ADDR = None
    # # SSL_CONFIG = dict(
    # #     cert='server.cer',
    # #     key='server.key',
    # #     password=None,
    # # )
    # SSL_CONFIG = None
    # LOGGING = None
    config = None

    def __init__(self, config):
        self.config = config
        if hasattr(config, 'LOGGING'):
            logging.config.dictConfig(config.LOGGING)

    def wsgi_app(self, environ, start_response):
        return self.connection_class(self).handle(environ, start_response)

    def run(self):
        kwargs = dict()

        if self.config.SSL_CONFIG:
            # 说明需要使用ssl
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(
                self.config.SSL_CONFIG['cert'],
                self.config.SSL_CONFIG['key'],
                self.config.SSL_CONFIG.get('password'),
            )
            kwargs['ssl_context'] = ssl_context

        server = WebSocketServer(
            self.config.PROXY_ADDR,
            self.wsgi_app,
            **kwargs
        )

        server.serve_forever()
