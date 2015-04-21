#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


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

