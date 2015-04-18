# -*- coding: utf-8 -*-
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import inspect
import json
import pyjsonrpc
from BaseHTTPServer import HTTPServer


def method(func):#, cli=True, rpc=True):
    if True or cli:
        func.cli_method = True
    if True or rpc:
        func.rpc_method = True
    return func


class Definition(object):

    def _get_rpc_methods(self):
        is_rpc_method = lambda i: 'rpc_method' in dir(i[1]) and i[1].rpc_method
        return dict(filter(is_rpc_method, inspect.getmembers(self)))

    def get_rpc_request_handler(self):
        class RequestHandler(pyjsonrpc.HttpRequestHandler):
            methods = self._get_rpc_methods()
        return RequestHandler

    @method#(rpc=False)
    def start_jsonrpc_server(self, hostname="localhost", port=8080):
        """ start json-rpc service """
        print "Starting %s json-rpc service at http://%s:%s" % (
            self.__class__.__name__, hostname, port
        )
        http_server = HTTPServer(
            server_address=(hostname, port),
            RequestHandlerClass=self.get_rpc_request_handler()
        )
        http_server.serve_forever()



