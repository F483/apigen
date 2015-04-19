######
apigen
######

Easily create a CLI and JSON-RPC interface from a common API definition.

============
Installation
============

::

    pip install apigen

======================
Example API definition
======================

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8
    # Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
    # License: MIT (see LICENSE file)


    import apigen


    class ExampleProgramm(apigen.Definition):
        """Example programm help text from class doc string."""

        def __init__(self, config="example.json", quiet=False):
            # programm positional and optional arguments taken from __init__ method
            # default argument of value False will be a flag in the cli
            pass

        @apigen.command()
        def example(self, positional_arg, optional_arg="example"):
            """Example command help text from method doc string."""
            # arguments without defaults are required positional arguments in th cli
            # arguments with default values will be optional in the cli
            return "positional_arg = %s, optional_arg = %s" % (
                positional_arg, optional_arg
            )

        @apigen.command(rpc=False) # don't show in rpc interface
        def clionly(self):
            """Command only visible in cli interface."""
            return "clionly"

        @apigen.command(cli=False) # don't show in cli interface
        def rpconly(self):
            """Command only visible in rpc interface."""
            return "rpconly"


    if __name__ == "__main__":
        apigen.run(ExampleProgramm) # run cli interface

=======================================
Generated cli interface (uses argparse)
=======================================

Programm interface and help text.

::

    $ python example.py -h
    usage: example.py [-h] [--config CONFIG] [--quiet] <command> ...

    Example programm help text from class doc string.

    optional arguments:
      -h, --help       show this help message and exit
      --config CONFIG  optional default=example.json
      --quiet          optional flag

    commands:
      <command>
        clionly        Command only visible in cli interface.
        jsonrpc        Start json-rpc service.
        example        Example command help text from method doc string.

Command interface and help text (jsonrpc command added by default).

::

    $ python example.py jsonrpc -h
    usage: example.py jsonrpc [-h] [--hostname HOSTNAME] [--port PORT]

    optional arguments:
      -h, --help           show this help message and exit
      --hostname HOSTNAME  optional default=localhost
      --port PORT          optional default=8080

==================================================
Generated json-rpc interface (uses python-jsonrpc)
==================================================

Starting the jsonrpc service from the command line.

::

    $ python example.py jsonrpc
    Starting ExampleProgramm json-rpc service at http://localhost:8080

Client site jsonrpc usage with python-jsonrpc.

.. code:: python

    import pyjsonrpc
    rpc = pyjsonrpc.HttpClient(url = "http://localhost:8080")
    print rpc.rpconly()

Starting the jsonrpc service from within python.

.. code:: python

    import example
    api = example.ExampleProgramm()
    api.jsonrpc()

Getting a pyjsonrpc.HttpRequestHandler for further use.

.. code:: python

    import example
    api = example.ExampleProgramm()
    api.get_http_request_handler()



