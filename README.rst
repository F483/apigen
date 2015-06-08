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

  # from examples/basic.py
  import apigen


  class Calculator(apigen.Definition):  # programm name taken from class name
      """example programm"""  # programm help text taken from class doc string.

      @apigen.command()
      def add(self, a, b):  # command name and args taken from method definition
          """adds two items"""  # help text taken from method doc string
          return a + b  # returned rpc and cli output (must be JSON serializable)


  if __name__ == "__main__":
      apigen.run(Calculator)  # run cli interface


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

  $ python examples/basic.py --help
  usage: example.py [-h] <command> ...

  example programm

  optional arguments:
    -h, --help  show this help message and exit

  commands:
    <command>
      add            adds two numbers
      startserver    Start json-rpc service.


Example command help text

::

  $ python examples/basic.py startserver --help
  usage: basic.py startserver [-h] [--hostname HOSTNAME] [--port PORT]

  optional arguments:
    -h, --help           show this help message and exit
    --hostname HOSTNAME  optional default=localhost
    --port PORT          optional default=8080


==================================================
Generated json-rpc interface (uses python-jsonrpc)
==================================================

Starting the jsonrpc server from the command line.

::

  $ python examples/basic.py startserver
  Starting Calculator json-rpc service at http://localhost:8080


Client site jsonrpc usage with python-jsonrpc.

.. code:: python

  import pyjsonrpc
  rpc = pyjsonrpc.HttpClient(url = "http://localhost:8080")
  print rpc.add(1, 2)


Starting the jsonrpc service from within python.

.. code:: python

  import basic
  api = basic.Calculator()
  api.startserver()


Getting a pyjsonrpc.HttpRequestHandler for further use.

.. code:: python

  import basic
  api = basic.Calculator()
  api.get_http_request_handler()



