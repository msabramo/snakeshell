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

'''Example tool one, hello world.'''

from sys import exit, stderr
from time import sleep
from random import sample

from snakeshell import HALT, CommandLineMapper

def hello(case='', shuffle='no', pace='0'):
    '''
    Emits a "Hello, world!" greeting message on standard error.

    Usage:

        python hello.py help
        python hello.py [case=upper/lower] [shuffle=yes/no] [pace=0]

    Arguments:

        help,              print this usage help and exit;
        case=upper/lower,  convert the message to lowercase or uppercase;
        shuffle=yes/no,    shuffle the letters of the message;
        pace=0,            greeting pace, in tenths of a second.

    Goodbye.
    '''

    if case in ['', 'upper', 'lower'] and shuffle in ['yes', 'no']:
        if pace.isdigit():
            words = ['Hello', 'world']
            delay = int(pace)

            if shuffle == 'yes':
                words[0] = ''.join(sample(words[0], len(words[0])))
                words[1] = ''.join(sample(words[1], len(words[1])))

            words = '{}, {}!'.format(*words)

            if case == 'upper':
                words = words.upper()

            elif case == 'lower':
                words = words.lower()

            if delay == 0:
                print(words, file=stderr)

            else:
                for x in words:
                    stderr.write(x)

                    stderr.flush()

                    sleep(delay / 10.0)

                print(file=stderr)

        else:
            return HALT

    else:
        return HALT

if __name__ == '__main__':
    cli = CommandLineMapper()

    cli.add(hello)

    if cli.run() is HALT:
        print(hello.__doc__, file=stderr)

        exit(1)
