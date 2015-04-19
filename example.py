#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import easyapi


class ExampleProgramm(easyapi.Definition):

    def __init__(self, config="example.json"):
        """Example programm help text."""
        # do something usefull with the programm arguments

    @easyapi.command()
    def showargs(self, positional_arg, optional_arg="example"):
        """returns the arguments passed"""
        return "showargs: %s %s" % (positional_arg, optional_arg)

    @easyapi.command()
    def testflag(self, quiet=False): # will add arg as flag if default is False
        """return text if quiet flag is not set"""
        if not quiet:
            return "something"
        return ""


if __name__ == "__main__":
    easyapi.run(ExampleProgramm) # run cli interface

