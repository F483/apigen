# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import argparse
import inspect
import pyjsonrpc
from BaseHTTPServer import HTTPServer


class VarargsFound(Exception):
    def __init__(self, command):
        msg = "command '%s' cannot use varargs" % command.__name__
        super(VarargsFound, self).__init__(msg)


class KeywordsFound(Exception):
    def __init__(self, command):
        msg = "command '%s' cannot use keywords" % command.__name__
        super(KeywordsFound, self).__init__(msg)


def command(cli=True, rpc=True):
    def decorator(func):
        func.cli_command = cli # set cli flag
        func.rpc_command = rpc # set rpc flag
        return func
    return decorator


class Definition(object):

    def get_http_request_handler(self):
        class RequestHandler(pyjsonrpc.HttpRequestHandler):
            methods = _get_rpc_commands(self)
        return RequestHandler

    @command(rpc=False)
    def jsonrpc(self, hostname="localhost", port=8080):
        """Start json-rpc service."""
        print "Starting %s json-rpc service at http://%s:%s" % (
            self.__class__.__name__, hostname, port
        )
        http_server = HTTPServer(
            server_address=(hostname, port),
            RequestHandlerClass=self.get_http_request_handler()
        )
        http_server.serve_forever()


def _get_rpc_commands(instance):
    is_rpc = lambda i: 'rpc_command' in dir(i[1]) and i[1].rpc_command
    return dict(filter(is_rpc, inspect.getmembers(instance)))


def _get_cli_commands(definition):
    is_cli = lambda i: 'cli_command' in dir(i[1]) and i[1].cli_command
    return dict(filter(is_cli, inspect.getmembers(definition)))


def _add_argument(parser, name, has_default, default):
    if has_default:
        if type(default) == type(True) and default == False: # add flag
            parser.add_argument('--%s' % name, action='store_true',
                                help="optional flag")
        else: # add optional argument
            parser.add_argument("--%s" % name, default=default, 
                                help="optional default=%s" % default)
    else: # add positional argument
        parser.add_argument(name, help="required")


def _add_arguments(parser, command):
    argspec = inspect.getargspec(command)
    if argspec.varargs: # no *args
        raise VarargsFound(command)
    if argspec.keywords: # no **kwargs
        raise KeywordsFound(command)
    args = argspec.args[1:] # exclude self
    defaults = argspec.defaults if argspec.defaults else []
    positional_count = len(args) - len(defaults)
    for i in range(len(args)):
        name = args[i]
        has_default = (i - positional_count) >= 0
        default = defaults[i - positional_count] if has_default else None
        _add_argument(parser, name, has_default, default)


def _get_init(definition):
    members = dict(inspect.getmembers(definition))
    init = members["__init__"]
    if type(init) == type(members["jsonrpc"]):
        return init # __init__ method was added
    return None


def _get_arguments(definition):

    # create parser
    if definition.__doc__:
        description = definition.__doc__
    else:
        description = "%s Command-line interface" % definition.__name__
    parser = argparse.ArgumentParser(description=description)

    # add programm args
    init = _get_init(definition)
    if init:
        _add_arguments(parser, init)

    # add command args
    subparsers = parser.add_subparsers(
        title='commands', dest='command', metavar="<command>"
    )
    commands = _get_cli_commands(definition)
    for name, command in commands.items():
        command_parser = subparsers.add_parser(name, help=command.__doc__)
        _add_arguments(command_parser, command)
    return vars(parser.parse_args())


def _pop_init_args(definition, kwargs):
    init_args = {}
    init = _get_init(definition)
    if not init:
        return init_args
    argnames = inspect.getargspec(init).args[1:] # exclude self
    for argname in argnames:
        init_args[argname] = kwargs.pop(argname)
    return init_args


def run(definition):
    kwargs = _get_arguments(definition)
    command_names = _get_cli_commands(definition).keys()
    instance = definition(**_pop_init_args(definition, kwargs))
    command = getattr(instance, kwargs.pop("command"))
    print command(**kwargs)


