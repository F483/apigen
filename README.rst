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

I simple example application with an add command.

.. code:: python

  # from examples/basic.py
  import apigen


  # automatically added verison command will use module version if present
  # rpc exceptions will also include module version if persent
  __version__ = "1.0.0"


  class Calculator(apigen.Definition):  # Programm name taken from class name.
      """Example Programm"""  # Programm help text taken from class doc string.

      @apigen.command()
      def add(self, a, b):  # Command name and args taken from method.
          """adds two items"""  # Help text taken from method doc string.
          return a + b  # Returned rpc/cli output (must be JSON serializable).


  if __name__ == "__main__":
      apigen.run(Calculator)  # Run CLI interface.


The created CLI/RPC interface behaves as you would expect from a python class.

 - Programm arguments are taken from the __init__ method.
 - Command arguments are taken from the respective command methods.
 - Manditory and optional arguments work just like you would expect in python.
 - In addition arguments with the default value False are flags in the CLI.

.. code:: python

  # from examples/arguments.py
  import apigen


  class ArgumentsExample(apigen.Definition):

      def __init__(self, quiet=False, config_path="default/path.json"):
          self.quiet = quiet
          self.config_path = config_path

      @apigen.command()
      def show_args(self, first, second, optional="Default"):
          if not self.quiet:
              print("noise")
          return { 'first': first, 'second': second, 'optional': optional }


  if __name__ == "__main__":
      apigen.run(ArgumentsExample)


=======================================
Generated CLI interface (uses argparse)
=======================================

Generated CLI interface.

::

  # Program, command and arguments order.
  $ python program.py [program arguments] <command> [command arguments]

  # Argument format.
  $ python program.py positional_argument_value --optional_argument=value --flag


Showing the generated help.

::

  # Show programm help text.
  $ python examples/basic.py --help

  # Show command help text
  $ python examples/basic.py startserver --help


CLI arguments must be given as json data.The json data automatically is
unmarshalled before calling the command function and the returned result is
automatically marshalled.

::

  $ python examples/basic.py add 1 2
  3

  $ python examples/basic.py add 1.1 2.2
  3.3000000000000003

  $ python examples/basic.py add "foo" "bar"
  "foobar"

  $ python examples/basic.py add "[1,2,3]" "[4,5,6]"
  [
    1,
    2,
    3,
    4,
    5,
    6
  ]



===============================================
Client side json-rpc usage with python-jsonrpc.
===============================================

Starting the jsonrpc server from the command line.

::

  $ python examples/basic.py startserver
  Starting Calculator json-rpc service at http://localhost:8080



RPC arguments must be given as json serializable data. The arguments will
automatically be marshalled and unmarshalled.

.. code:: python


  >>> import pyjsonrpc

  >>> rpc = pyjsonrpc.HttpClient(url = "http://localhost:8080")

  >>> rpc.add(1, 2)
  3

  >>> rpc.add(1.1, 2.2)
  3.3000000000000003

  >>> rpc.add("foo", "bar")
  u'foobar'

  >>> rpc.add([1,2,3], [4,5,6])
  [1, 2, 3, 4, 5, 6]


Client side exception handeling.

.. code:: python

  # from examples/exceptions.py
  import json
  import pyjsonrpc


  rpc = pyjsonrpc.HttpClient(url="http://localhost:8080")
  try:
      print rpc.add(1, "str")
  except pyjsonrpc.rpcerror.JsonRpcError as e:
      print e.code  # see http://www.jsonrpc.org/specification#error_object

      # Server error if an exception is raised during the call.
      if e.code <= -32000 and e.code >= -32099:
          print e.message  # source exception message
          data = json.loads(e.data)
          print data["classname"]  # source exception class name
          print data["repr"]  # source exception repr string
          print data["traceback"]  # source exception traceback
          print data["version"]  # source module version if present


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


==========================================
Client side json-rpc usage with javascript
==========================================

.. code:: javascript

  // from examples/node.js

  // https://www.npmjs.com/package/node-json-rpc
  // npm install node-json-rpc
  var rpc = require('node-json-rpc');

  var client = new rpc.Client({
        port: 8080,
        host: '127.0.0.1',
        path: '/',
  });

  client.call({
      "jsonrpc": "2.0",
      "method": "add",
      "params": {
        a: 1,
        b: 3
      },
      "id": 0
    },
    function(err, res) {
      if (err) {
        console.log("Error add");
        console.log(err);
      } else {
        console.log("Success add");
        console.log(res);
      }
    }
  );

::

  $ node examples/node.js
  Success add
  { jsonrpc: '2.0', id: 0, result: 4 }
