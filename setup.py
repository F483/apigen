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
    keywords=("CLI, JSON, RPC, JSON-RPC, API, Remote Procedure Call, "
              "JavaScript Object Notation, argparse, Data Interchange"),
    url='https://github.com/F483/apigen/',
    author='Fabian Barkhau',
    author_email='fabian.barkhau@gmail.com',
    license='MIT',
    packages=find_packages(),
    download_url = DOWNLOAD_URL,
    #test_suite="tests",
    install_requires=[
        'python-jsonrpc == 0.7.7',
        'argparse == 1.2.1',
    ],
    tests_require=[
        'coverage',
        'coveralls',
        'ipython',
        'pudb'  # import pudb; pu.db # set break point
    ],
    zip_safe=False,
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
