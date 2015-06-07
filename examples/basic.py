#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import apigen
from decimal import Decimal


class Calculator(apigen.Definition):  # programm name taken from class name
    """example programm"""  # programm help text taken from class doc string.

    @apigen.command()
    def add(self, a, b):  # command name and args taken from method definition
        """adds two numbers"""  # help text taken from method doc string
        result = float(Decimal(a) + Decimal(b))
        return result  # return rpc and cli output (must be JSON serializable)


if __name__ == "__main__":
    apigen.run(Calculator)  # run cli interface
