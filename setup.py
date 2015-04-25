#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import os
from setuptools import setup, find_packages


THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)


VERSION = open("version.txt").readline().strip()
DOWNLOAD_BASEURL = "https://pypi.python.org/packages/source/a/apigen/"
DOWNLOAD_URL = DOWNLOAD_BASEURL + "apigen-%s.tar.gz" % VERSION


setup(
    name='apigen',
    version=VERSION,
    description=('Easily create a CLI and JSON-RPC interface '
                 'from a common API definition.'),
    long_description=open("README.rst").read(),
    keywords=("CLI, JSON, RPC, JSON-RPC, API, argparse, Remote Procedure Call, "
              "JavaScript Object Notation, Data Interchange"),
    url='https://github.com/F483/apigen/',
    author='Fabian Barkhau',
    author_email='fabian.barkhau@gmail.com',
    license='MIT',
    packages=find_packages(),
    download_url = DOWNLOAD_URL,
    #test_suite="tests",
    install_requires=[
        'python-jsonrpc == 0.7.3',
        'argparse == 1.2.1'
    ],
    tests_require=[ # TODO how to install it?
      'ipython',
      'pudb' # import pudb; pu.db # set break point
      # TODO lint and static analisys
    ],
    zip_safe=False
)


