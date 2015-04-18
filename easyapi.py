# -*- coding: utf-8 -*-
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import argparse
import inspect
import json
import pyjsonrpc
from BaseHTTPServer import HTTPServer


def command(func):#, cli=True, rpc=True):
    if True or cli: # flag as cli command
        func.cli_command = True
    if True or rpc: # flag as rpc command
        func.rpc_command = True
    return func


class Definition(object):

    def _get_rpc_commands(self):
        is_rpc = lambda i: 'rpc_command' in dir(i[1]) and i[1].rpc_command
        return dict(filter(is_rpc, inspect.getmembers(self)))

    def get_rpc_request_handler(self):
        class RequestHandler(pyjsonrpc.HttpRequestHandler):
            commands = self._get_rpc_commands()
        return RequestHandler

    @command#(rpc=False)
    def jsonrpc_service(self, hostname="localhost", port=8080):
        """start json-rpc service"""
        print "Starting %s json-rpc service at http://%s:%s" % (
            self.__class__.__name__, hostname, port
        )
        http_server = HTTPServer(
            server_address=(hostname, port),
            RequestHandlerClass=self.get_rpc_request_handler()
        )
        http_server.serve_forever()


def _get_cli_commands(definition):
    is_cli = lambda i: 'cli_command' in dir(i[1]) and i[1].rpc_command
    return dict(filter(is_cli, inspect.getmembers(definition)))


def _get_arguments(definition):
    parser = argparse.ArgumentParser()
    # TODO add app args
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    commands = _get_cli_commands(definition)
    for name, command in commands.items():
        command_parser = subparsers.add_parser(
            name, help=command.__doc__
        )
    return parser.parse_args()


def run(definition):
    args = _get_arguments(definition)
    command_names = _get_cli_commands(definition).keys()
    instance = definition() # TODO use app args
    kwargs = vars(args)
    command = getattr(instance, kwargs.pop("command"))
    print command(**kwargs)


