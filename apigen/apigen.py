# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


from __future__ import print_function
from __future__ import unicode_literals
import json
import sys
import signal
import argparse
import inspect
import pyjsonrpc
from BaseHTTPServer import HTTPServer


class ApigenArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


class VarargsFound(Exception):

    def __init__(self, command):
        msg = "command '%s' cannot use varargs" % command.__name__
        super(VarargsFound, self).__init__(msg)


class KeywordsFound(Exception):

    def __init__(self, command):
        msg = "command '%s' cannot use keywords" % command.__name__
        super(KeywordsFound, self).__init__(msg)


_command_num = 0


def command(cli=True, rpc=True):
    def decorator(func):
        global _command_num
        func.apigen_cli = cli  # set cli flag
        func.apigen_rpc = rpc  # set rpc flag
        func.apigen_num = _command_num  # set ordering flag
        _command_num += 1
        return func
    return decorator


class Definition(object):

    def get_http_request_handler(self):
        class RequestHandler(pyjsonrpc.HttpRequestHandler):
            methods = _get_rpc_commands(self)
        return RequestHandler

    @command(rpc=False)
    def startserver(self, hostname="localhost", port=8080, daemon=False):
        """Start json-rpc service."""
        if daemon:
            print("Sorry daemon server not supported just yet.")
            # TODO start as daemon similar to bitcoind
        else:
            print("Starting %s json-rpc service at http://%s:%s" % (
                self.__class__.__name__, hostname, port
            ))
            http_server = HTTPServer(
                server_address=(hostname, int(port)),
                RequestHandlerClass=self.get_http_request_handler()
            )

            def sigint_handler(signum, frame):
                #http_server.shutdown() # FIXME why does it block?
                sys.exit(0)
            signal.signal(signal.SIGINT, sigint_handler)
            http_server.serve_forever()

    @command()
    def stopserver(self, hostname="localhost", port=8080):
        """Stop json-rpc service."""
        print("Sorry stop server not supported just yet.")
        # TODO implement


def _get_rpc_commands(instance):
    is_rpc = lambda i: 'apigen_rpc' in dir(i[1]) and i[1].apigen_rpc
    return dict(filter(is_rpc, inspect.getmembers(instance)))


def _get_cli_commands(definition):
    is_cli = lambda i: 'apigen_cli' in dir(i[1]) and i[1].apigen_cli
    return dict(filter(is_cli, inspect.getmembers(definition)))


def _add_argument(parser, name, has_default, default):
    if has_default:
        if isinstance(default, bool) and default is False:  # add flag
            parser.add_argument('--%s' % name, action='store_true',
                                help="optional flag")
        else:  # add optional argument
            parser.add_argument("--%s" % name, default=default,
                                help="optional default=%s" % default)
    else:  # add positional argument
        parser.add_argument(name, help="required")


def _add_arguments(parser, command):
    argspec = inspect.getargspec(command)
    if argspec.varargs:  # no *args
        raise VarargsFound(command)
    if argspec.keywords:  # no **kwargs
        raise KeywordsFound(command)
    args = argspec.args[1:]  # exclude self
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
    if type(init) == type(members["startserver"]):
        return init  # __init__ method was added
    return None


def _get_arguments(definition):

    # create parser
    if definition.__doc__:
        description = definition.__doc__
    else:
        description = "%s Command-line interface" % definition.__name__
    parser = ApigenArgumentParser(description=description)

    # add programm args
    init = _get_init(definition)
    if init:
        _add_arguments(parser, init)

    # add command args
    subparsers = parser.add_subparsers(
        title='commands', dest='command', metavar="<command>"
    )
    itmes = _get_cli_commands(definition).items()
    for name, command in sorted(itmes, key=lambda item: item[1].apigen_num):
        command_parser = subparsers.add_parser(name, help=command.__doc__)
        _add_arguments(command_parser, command)
    return vars(parser.parse_args())


def _pop_init_args(definition, kwargs):
    init_args = {}
    init = _get_init(definition)
    if not init:
        return init_args
    argnames = inspect.getargspec(init).args[1:]  # exclude self
    for argname in argnames:
        init_args[argname] = kwargs.pop(argname)
    return init_args


def _deserialize(kwargs):
    def deserialize(item):
        if isinstance(item[1], str):
            try:
                data = json.loads(item[1])  # load as json
            except:
                data = item[1].decode('utf-8')  # must be a string
        else:
            data = item[1]  # already deserialized default value
        return (item[0], data)
    return dict(map(deserialize, kwargs.items()))


def run(definition):
    kwargs = _get_arguments(definition)
    kwargs = _deserialize(kwargs)
    instance = definition(**_pop_init_args(definition, kwargs))
    command = getattr(instance, kwargs.pop("command"))
    print(json.dumps(command(**kwargs), indent=2, ensure_ascii=False))
