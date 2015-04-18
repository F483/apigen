#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)

import easyapi

class Example(easyapi.Definition):

    @easyapi.command
    def test_command(self, positional, optional="default"):
        return "test_command: %s %s" % (positional, optional)

    @easyapi.command
    def test_cli(self):
        """Test the command line interface"""
        return "test_cli"


easyapi.run(Example)
