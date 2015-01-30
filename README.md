# snakeshell

Snakeshell is a command line “parser” (mapper). What it really does is expose
Python functions to the shell. Main features:

* Very small codesize. A single Python module. About a hundred lines of code.
* The public API consists of a Python class, `CommandLineMapper`; plus two
  methods, `add` and `run`.
* No external dependencies.
* Support for Python 3 (version 2 is comming).

## Installation

To install Snakeshell, type the following command.

    pip install snakeshell

## Basic Use

Snakeshell performs a direct mapping of command line arguments to an exposed
Python function. Consider the snippet below.

```python
from snakeshell import CommandLineMapper

def myfunc(arg1, arg2, arg3='val'):
    print(arg1)
    print(arg2)
    print(arg3)

if __name__ == '__main__':
    cli = CommandLineMapper()

    cli.add(myfunc)

    cli.run()
```

The last three instructions demonstrate the basic operation of the API.

1. Instantiate the `CommandLineMapper`.

2. Register the function you want to expose, using the `CommandLineMapper.add`
method.

3. Call `CommandLineMapper.run`. At this point Snakeshell will process the
command line, `sys.argv`, and invoke the matching function.

Suppose the above snippet is saved as `myscript.py`.

    $ python myscript.py val1 val2 arg3=val3
    val1
    val2
    val3

The output reveals that the shell command above actually called
`myfunc('val1', 'val2', arg3='val3')`. A couple of notices.

1. Only one function was exposed via `CommandLineMapper.add`, so its name could
be ommited from the command line. If exposing more than one function, it is
recommended to pass its name as the first program argument, otherwise the first
exposed function will be called. See next section.

2. There is no type validation/coersion. Snakeshell will only pass strings on
function calls.

## Multiple Commands

If your script is large you can organize it as a suite of sub-commands. Create
one function for each command you expect to handle and register all of them
with `CommandLineMapper.add`. Consider the pseudo-code below.

```python

def subcommand1(*args1, **kwargs1):
    pass

def subcommand2(*args2, **kwargs2):
    pass

if __name__ == '__main__':
    cli = CommandLineMapper()

    cli.add(subcommand1)
    cli.add(subcommand2)

    cli.run()
```

You can then specify which function to run via command line. For example, to
invoke `subcommand2` with arguments `val1` and `val2`, type the following.

    python mysuite.py subcommand2 val1 val2

Notice that the `subcommand2` entry itself is extracted from the argument
line. The remainder of the line is processed as usual. In this case, `args2`
is `['val1', 'val2']`.

## Complete example

Here is a complete example.

```python
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
```

Observe that the **hello** function does not have a **help** argument, but the
**docstring** says different. The **help** argument is automatically recognized
and, if provided, will cause Snakeshell to print the **docstring** of the
**hello** function. A default help text will be printed if a function does not
supply a **docstring**.

The call to `CommandLineMapper.run` will return **HALT** if a command is
invoked with an invalid syntax. Your functions can also use it to signal error
conditions. This allows the program to exit with a non-zero status, or trigger
some error handling function.

## Q&A

Q. I want POSIX arguments.

A. Wrong tool. There are plenty of Pyhthon command line parsing utilities
supporting POSIX. Try one of them.

* Argparse/Optparse/Getopt. Built into Python. Complex.
* [Compago](https://github.com/jmohr/compago). Very nice, but
  unmaintained. Also, does not run on Python 3.
* [Docopt](http://docopt.org/).
* [Clint](https://github.com/kennethreitz/clint).
* [Click](http://click.pocoo.org/3/).

Q. I need type coersion.

A. Implement it yourself, or use some third party library.

Q. I can use Python itself as a command line interpreter. Why all of this?

A. Yes you can. In this case all of this becomes irrelevant. I prefer not to,
that is one of the reasons I wrote this tool. Another is that everything else
is too complex. YMMV.

Q. Why not use `sys.argv` directly.

A. Good question. I do this a lot of times. Actually, if your script is small
enought and requires zero, one, or maybe two positional parameters, there is no
need for command line processing tools. Write a couple of conditionals and
print a simple help message in case of errors.

