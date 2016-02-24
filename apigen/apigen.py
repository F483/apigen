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
import traceback
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


def _get_version(cmd_self):
    cmd_module_name = cmd_self.__class__.__module__
    cmd_module = sys.modules[cmd_module_name]
    if hasattr(cmd_module, '__version__'):
        return cmd_module.__version__
    return ""


def command(cli=True, rpc=True):
    def decorator(func):
        global _command_num

        # wrap func for rpc exception handeling
        def wrapper(*args, **kwargs):
            if args[0]._http_server is None:  # cli or python call
                return func(*args, **kwargs)
            else:  # rpc call
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    code = -32000  # -32000 to 32099
                    msg = e.message
                    data = json.dumps({
                        "traceback": traceback.format_exc(),
                        "classname": e.__class__.__name__,
                        "version": _get_version(args[0]),
                        "repr": repr(e)
                    })
                    raise pyjsonrpc.rpcerror.JsonRpcError(msg, data, code)

        # add flags to wrapper
        wrapper.apigen_cli = cli  # set expose cli flag
        wrapper.apigen_rpc = rpc  # set expose rpc flag
        wrapper.apigen_num = _command_num  # set cli ordering flag
        wrapper.apigen_src = func  # attach func to get argument later

        _command_num += 1
        return wrapper
    return decorator


class Definition(object):

    _http_server = None

    def get_http_request_handler(self):
        class RequestHandler(pyjsonrpc.HttpRequestHandler):
            methods = _get_rpc_commands(self)
        return RequestHandler

    @command()
    def version(self):
        """Returns the current software version!"""
        # FIXME return something usefull if no __version__ property
        return _get_version(self)

    def _post_shutdown(self):

        # call stop server handler if exists
        if('on_shutdown' in dir(self) and
                callable(self.on_shutdown)):
            self.on_shutdown()

        # for backwards compatibility
        elif('on_stop_server' in dir(self) and
                callable(self.on_stop_server)):
            print("DEPRECATED on_stop_server! Use on_shutdown instead.")
            self.on_stop_server()

    def stopserver(self):
        assert(self._http_server is not None)
        self._http_server.shutdown()
        self._post_shutdown()

    @command(rpc=False)
    def startserver(self, hostname="localhost", port=8080,
                    daemon=False, handle_sigint=True):
        """Start json-rpc service."""
        if daemon:
            print("Sorry daemon server not supported just yet.")
            # TODO start as daemon similar to bitcoind
        else:
            print("Starting %s json-rpc service at http://%s:%s" % (
                self.__class__.__name__, hostname, port
            ))
            self._http_server = HTTPServer(
                server_address=(hostname, int(port)),
                RequestHandlerClass=self.get_http_request_handler()
            )

            if handle_sigint:
                def sigint_handler(signum, frame):
                    self._post_shutdown()
                    sys.exit(0)
                signal.signal(signal.SIGINT, sigint_handler)
            self._http_server.serve_forever()


def _get_rpc_commands(instance):

    def is_rpc(i):
        return 'apigen_rpc' in dir(i[1]) and i[1].apigen_rpc
    return dict(filter(is_rpc, inspect.getmembers(instance)))


def _get_cli_commands(definition):

    def is_cli(i):
        return 'apigen_cli' in dir(i[1]) and i[1].apigen_cli
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
    argspec = inspect.getargspec(command.apigen_src)
    if argspec.varargs:  # no *args
        raise VarargsFound(command.apigen_src)
    if argspec.keywords:  # no **kwargs
        raise KeywordsFound(command.apigen_src)
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

    # check if __init__ method was added
    if type(init) == type(members["startserver"]): # NOQA
        # wrap init so _add_arguments works
        def wrapper(*args, **kwargs):
            return init(*args, **kwargs)
        wrapper.apigen_src = init
        return wrapper
    return None


def _get_arguments(definition, args):

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
        helptext = command.apigen_src.__doc__
        command_parser = subparsers.add_parser(name, help=helptext)
        _add_arguments(command_parser, command)
    return vars(parser.parse_args(args=args))


def _pop_init_args(definition, kwargs):
    init_args = {}
    init = _get_init(definition)
    if not init:
        return init_args
    argnames = inspect.getargspec(init.apigen_src).args[1:]  # exclude self
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
            data = item[1]  # already deserialized (method default value)
        return (item[0], data)
    return dict(map(deserialize, kwargs.items()))


def run(definition, args=None):
    if args is None:
        args = sys.argv[1:]
    kwargs = _get_arguments(definition, args)
    kwargs = _deserialize(kwargs)
    instance = definition(**_pop_init_args(definition, kwargs))
    command = getattr(instance, kwargs.pop("command"))
    try:
        result = command(**kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False))  # allow unicode
    finally:
        if('on_shutdown' in dir(instance) and callable(instance.on_shutdown)):
            instance.on_shutdown()
