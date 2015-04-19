#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


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

