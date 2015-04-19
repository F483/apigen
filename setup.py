# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import os
from setuptools import setup, find_packages


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PROJECT_DIR, 'README.rst')) as f:
    README = f.read()


setup(
    name='apigen',
    version='0.1.1',
    description=('Easily create a CLI and JSON-RPC interface '
                 'from a common API definition.'),
    long_description=README,
    keywords="cli json rpc api argparse",
    url='https://github.com/F483/apigen/',
    author='Fabian Barkhau',
    author_email='fabian.barkhau@gmail.com',
    license='MIT',
    packages=find_packages(),
    download_url = "https://pypi.python.org/packages/source/a/apigen/apigen-0.1.1.tar.gz",
    #test_suite="tests",
    install_requires=[
        'python-jsonrpc == 0.7.3'
    ],
    zip_safe=False
)


