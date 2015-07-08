#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


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
    apigen.run(Calculator)  # Run cli interface.
