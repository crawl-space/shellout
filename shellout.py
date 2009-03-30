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

"""
shellout provides an OO-like interface to running shell commands.

Example::
    import shellout as so
    print so.echo("hello, world")
"""


import sys

class ShellOutQuoter(object):
    def _shell_safe_string(self, *args):
        def quote(s):
            s = s.replace('\\','\\\\') # escape backslashes
            s = s.replace('"','\\"')   # escape double quotes
            return '"%s"' % (s,)
        return ' '.join(map(quote, args))


class ShellError(OSError):

    def __init__(self, command, exit_code, output):
        self.command = command
        self.exit_code = exit_code
        self.output = output
    
    def __str__(self):
        return "Command '%s' failed with exit code %s:\n%s" % (
            self.command,
            self.exit_code,
            self.output)

class ShellOutArg(ShellOutQuoter):

    def __init__(self, cmd_string, arg_name):
        self._cmd_string = cmd_string
        self._arg_value = None
        if len(arg_name) == 1:
            self._arg = "-" + arg_name
            self._arg_fmt_string = self._arg + " %s"
        else:
            self._arg = "--" + arg_name
            self._arg_fmt_string = self._arg + "=%s"

    def _set_arg_value(self, arg):
        if self._arg_value is not None:
            raise ValueError("option %s already set to \"%s\"" % (self._arg,))
        self._arg_value = arg
        self._arg = self._arg_fmt_string % (self._shell_safe_string(arg),)

    def __getattr__(self, x):
        return self.__class__(str(self), x)

    def __getitem__(self, arg):
        self._set_arg_value(arg)
        return self
    
    def __str__(self):
        return self._cmd_string + " " + self._arg

    def __call__(self, *args):
        import commands
        cmd = str(self)
        if len(args) > 0:
            cmd += " " + self._shell_safe_string(*args)
        return commands.getoutput(cmd)


class ShellOutCommand(ShellOutQuoter):

    _soa = ShellOutArg
    ShellError = ShellError

    def __init__(self, cmd):
        self._cmd = cmd

    def __getattr__(self, x):
        return self._soa(self._cmd, x)

    def __call__(self, *args):
        import commands
        to_run = self._cmd + ' ' + self._shell_safe_string(*args)
        results = commands.getstatusoutput(to_run)
        if results[0] != 0:
            raise self.ShellError(to_run, *results)
        return results[1]


class ShellOutModule(object):

    # Hack this in so we can still describe the module at the top of the file
    __doc__ = sys.modules[__name__].__doc__

    def __init__(self):
        self._soc = ShellOutCommand
        self._soa = ShellOutArg

    def __getattr__(self, x):
        return self._soc(x)


sys.modules[__name__] = ShellOutModule()
