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

    import apigen
    from decimal import Decimal


    class Calculator(apigen.Definition): # programm name taken from class name
        """example programm""" # programm help text taken from class doc string.

        @apigen.command()
        def add(self, a, b): # command name and args taken from method definition
            """adds two numbers""" # help text taken from method doc string
            result = Decimal(a) + Decimal(b)
            print result # cli interface uses stdout and errout
            return result # rpc interface uses value returned by method


    if __name__ == "__main__":
        apigen.run(Calculator) # run cli interface


=======================================
Generated cli interface (uses argparse)
=======================================

Program, command and arguments order.

::

    program [program arguments] <command> [command arguments] 


Argument format.

::

    program positionalargvalue --optionalarg=value --flag



Example programm help text.

::

    $ python examples/basicexample.py --help
    usage: example.py [-h] <command> ...

    example programm

    optional arguments:
      -h, --help  show this help message and exit

    commands:
      <command>
        add       adds two numbers
        jsonrpc   Start json-rpc service.


Example command help text

::


    $ python examples/basicexample.py jsonrpc --help
    usage: basicexample.py jsonrpc [-h] [--hostname HOSTNAME] [--port PORT]

    optional arguments:
      -h, --help           show this help message and exit
      --hostname HOSTNAME  optional default=localhost
      --port PORT          optional default=8080


==================================================
Generated json-rpc interface (uses python-jsonrpc)
==================================================

Starting the jsonrpc service from the command line.

::

    $ python examples/basicexample.py jsonrpc
    Starting Calculator json-rpc service at http://localhost:8080


Client site jsonrpc usage with python-jsonrpc.

.. code:: python

    import pyjsonrpc
    rpc = pyjsonrpc.HttpClient(url = "http://localhost:8080")
    print rpc.add(1, 2)


Starting the jsonrpc service from within python.

.. code:: python

    import basicexample
    api = basicexample.Calculator()
    api.jsonrpc()


Getting a pyjsonrpc.HttpRequestHandler for further use.

.. code:: python

    import basicexample
    api = basicexample.Calculator()
    api.get_http_request_handler()



