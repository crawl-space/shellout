# Copyright (c) 2009 James Bowes <jbowes@dangerouslyinc.com>
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


class ShellOutArg(object):

    def __init__(self, cmd_string, arg_name):
        self._cmd_string = cmd_string
        self._arg = None
        if len(arg_name) == 1:
            self._arg_name = " -" + arg_name
            self._longopt = False
        else:
            self._arg_name = " --" + arg_name
            self._longopt = True
        self._called = False

    def __getattr__(self, x):
        cmd = self._cmd_string + self._arg_name
        if self._arg:
            if self._longopt:
                cmd += "="
            else:
                cmd += " "
            cmd += "\"%s\"" % self._arg

        return self.__class__(cmd, x)

    def __getitem__(self, arg):
        self._arg = arg
        self._called = True
        return self

    def __call__(self, *args):
        import commands

        cmd = self._cmd_string + self._arg_name
        if self._arg:
            if self._longopt:
                cmd += "="
            else:
                cmd += " "
            cmd += "\"%s\"" % self._arg
        if len(args) > 0:
            cmd += " " + " ".join(['"%s"' % x for x in args])

        return commands.getoutput(cmd)


class ShellOutCommand(object):

    _soa = ShellOutArg

    def __init__(self, cmd):
        self._cmd = cmd

    def __getattr__(self, x):
        return self._soa(self._cmd, x)

    def __call__(self, *args):
        import commands

        to_run = self._cmd + " " + " ".join(['"%s"' % x for x in args])

        results = commands.getstatusoutput(to_run)
        if results[0] != 0:
            raise OSError(results)
        return results[1]


class ShellOutModule(object):

    def __init__(self):
        self._soc = ShellOutCommand
        self._soa = ShellOutArg

    def __getattr__(self, x):
        return self._soc(x)


import sys
sys.modules[__name__] = ShellOutModule()
