# easyapi

Easily create a CLI and JSON-RPC interface from a common API definition.

## Installation

    pip install easyapi

## Example API definition

    import easyapi


    class ExampleProgramm(easyapi.Definition):

        def __init__(self, config="example.json", quiet=False):
            """Example programm help text from init doc string."""
            # programm positional and optional arguments taken from __init__ method
            # default argument of value False will be a flag in the cli

        @easyapi.command()
        def example(self, positional_arg, optional_arg="example"):
            """Example command help text from method doc string."""
            # arguments without defaults are required positional arguments in th cli
            # arguments with default values will be optional in the cli
            return "positional_arg = %s, optional_arg = %s" % (
                positional_arg, optional_arg
            )

        @easyapi.command(rpc=False) # don't show in rpc interface
        def clionly(self):
            """Command only visible in cli interface."""
            return "clionly"

        @easyapi.command(cli=False) # don't show in cli interface
        def rpconly(self):
            """Command only visible in rpc interface."""
            return "rpconly"


    if __name__ == "__main__":
        easyapi.run(ExampleProgramm) # run cli interface

## Generated cli interface (uses argparse)

Programm interface and help text.

    $ python example.py -h
    usage: example.py [-h] [--config CONFIG] [--quiet] <command> ...

    Example programm help text from init doc string.

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

    $ python example.py jsonrpc -h
    usage: example.py jsonrpc [-h] [--hostname HOSTNAME] [--port PORT]

    optional arguments:
      -h, --help           show this help message and exit
      --hostname HOSTNAME  optional default=localhost
      --port PORT          optional default=8080

## Generated json-rpc interface (uses python-jsonrpc)

Starting the jsonrpc service from the command line.

    $ python example.py jsonrpc
    Starting ExampleProgramm json-rpc service at http://localhost:8080

Client site jsonrpc usage.

    > import pyjsonrpc
    > http_client = pyjsonrpc.HttpClient(url = "http://localhost:8080")
    > print http_client.rpconly()
    rpconly

Starting the jsonrpc service from within python.

    > import example
    > api = example.ExampleProgramm()
    > api.jsonrpc()
    Starting ExampleProgramm json-rpc service at http://localhost:8080

Getting a HttpRequestHandler for further use.

    > import example
    > api = example.ExampleProgramm()
    > api.get_http_request_handler()



