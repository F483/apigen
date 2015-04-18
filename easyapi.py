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

    def get_rpc_request_handler(self):
        class RequestHandler(pyjsonrpc.HttpRequestHandler):
            commands = _get_rpc_commands(self)
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


def _get_rpc_commands(instance):
    is_rpc = lambda i: 'rpc_command' in dir(i[1]) and i[1].rpc_command
    return dict(filter(is_rpc, inspect.getmembers(instance)))

def _get_cli_commands(definition):
    is_cli = lambda i: 'cli_command' in dir(i[1]) and i[1].rpc_command
    return dict(filter(is_cli, inspect.getmembers(definition)))


def _add_argument(parser, name, has_default, default):
    if has_default:
        parser.add_argument("--%s" % name, default=default, 
                            help="optional (default=%s)" % default)
    else:
        parser.add_argument(name, help="required")



def _add_arguments(parser, command):
    argspec = inspect.getargspec(command)
    if argspec.varargs: # no *args
        raise Exception("varargs not supported: %s" % command.__name__)
    if argspec.keywords: # no **kwargs
        raise Exception("keywords not supported: %s" % command.__name__)
    # TODO limit default types
    args = argspec.args[1:] # exclude self
    defaults = argspec.defaults if argspec.defaults else []
    positional_count = len(args) - len(defaults)
    for i in range(len(args)):
        name = args[i]
        has_default = (i - positional_count) >= 0
        default = defaults[i - positional_count] if has_default else None
        _add_argument(parser, name, has_default, default)


def _get_arguments(definition):
    parser = argparse.ArgumentParser()
    # TODO add app args
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    commands = _get_cli_commands(definition)
    for name, command in commands.items():
        command_parser = subparsers.add_parser(name, help=command.__doc__)
        _add_arguments(command_parser, command)
    return parser.parse_args()


def run(definition):
    args = _get_arguments(definition)
    command_names = _get_cli_commands(definition).keys()
    instance = definition() # TODO use app args
    kwargs = vars(args)
    command = getattr(instance, kwargs.pop("command"))
    print command(**kwargs)


