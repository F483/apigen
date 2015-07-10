#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import apigen


class ReturnNull(apigen.Definition):

    @apigen.command()
    def test(self):
        return None


if __name__ == "__main__":
    apigen.run(ReturnNull)
