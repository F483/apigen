#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import apigen


class ArgumentsExample(apigen.Definition):

    def __init__(self, quiet=False, config_path="default/path.json"):
        self.quiet = quiet
        self.config_path = config_path

    @apigen.command()
    def show_args(self, first, second, optional="Default"):
        if not self.quiet:
            print("noise")
        return {'first': first, 'second': second, 'optional': optional}

    @apigen.command()
    def arg_type(self, arg):
        return str(type(arg))

    def on_shutdown(self):
        print "called on stop"


if __name__ == "__main__":
    apigen.run(ArgumentsExample)
