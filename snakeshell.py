# -*- coding: utf-8; -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Rafael Viotti
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from sys import argv, stderr
from inspect import trace, getmodule

HALT = object()

class CommandLineMapper:
    def __init__(self):
        self._funcs = []

    def add(self, function):
        self._funcs.append(function)

        return function

    def run(self):
        if len(self._funcs) >= 1:
            fun = self._funcs[0]
            lst = []
            dic = {}

            if len(self._funcs) > 1:
                gen = (x for x in self._funcs if x.__name__ == argv[1])
                fun = next(gen, fun)

            if len(argv) > 1 and fun.__name__ == argv[1]:
                argv.remove(fun.__name__)

            if len(argv) == 1 or argv[1] != 'help':
                for opt in argv[1:]:
                    if '=' in opt:
                        key, val = opt.split('=', 1)

                        dic[key] = val

                    else:
                        lst.append(opt)

                try:
                    return fun(*lst, **dic)

                except TypeError:
                    frm = trace()[-1]
                    mod = getmodule(frm[0])

                    if mod and mod.__name__ == __name__:
                        if fun.__doc__ is not None:
                            print(fun.__doc__, file=stderr)

                        else:
                            pass  # TODO: print a default synopsis.

                        return HALT

                    else:
                        raise

            else:
                if fun.__doc__ is not None:
                    print(fun.__doc__, file=stderr)

                else:
                    pass  # TODO: print a default synopsis.

                return HALT

        else:
            raise Exception()

