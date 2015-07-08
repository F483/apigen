#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


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
