#!/usr/bin/env python
# coding: utf-8


from setuptools import setup, find_packages


exec(open('apigen/version.py').read())  # load __version__


setup(
    name='apigen',
    description=('Easily create a CLI and JSON-RPC interface '
                 'from a common API definition.'),
    long_description=open("README.rst").read(),
    keywords=("CLI, JSON, RPC, JSON-RPC, API, Remote Procedure Call, "
              "JavaScript Object Notation, argparse, Data Interchange"),
    url='https://github.com/F483/apigen/',
    author='Fabian Barkhau',
    author_email='fabian.barkhau@gmail.com',
    license="MIT",
    version=__version__,  # NOQA
    test_suite="tests",
    dependency_links=[],
    install_requires=open("requirements.txt").readlines(),
    tests_require=open("test_requirements.txt").readlines(),
    packages=find_packages(),
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
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
