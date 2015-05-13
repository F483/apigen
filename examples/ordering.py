#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import apigen
from decimal import Decimal


class Ordering(apigen.Definition):

    @apigen.command()
    def first(self):
        return "first"

    @apigen.command()
    def second(self):
        return "second"

    @apigen.command()
    def third(self):
        return "third"

    @apigen.command()
    def fourth(self):
        return "fourth"


if __name__ == "__main__":
    apigen.run(Ordering) 

