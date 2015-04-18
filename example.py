#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)

import easyapi

class Example(easyapi.Definition):

    @easyapi.method
    def test_method(self, positional, optional="default"):
        return "test_method: %s %s" % (positional, optional)


example = Example()
example.start_jsonrpc_server()

