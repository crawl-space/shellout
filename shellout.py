#!/usr/bin/python

class ShellOutArg(object):

    def __init__(self, cmd_string, arg_name):
        self._cmd_string = cmd_string
        if len(arg_name) == 1:
            self._arg_name = " -" + arg_name
        else:
            self._arg_name = " --" + arg_name
        self._called = False

    def __getattr__(self, x):
        cmd_string = self._cmd_string + self._arg_name + " " + " ".join(self._args)
        return self.__class__(cmd_string, x)

    def __call__(self, *args):
        if not self._called:
            self._args = args
            self._called = True
            return self
        else:
            import commands

            cmd = self._cmd_string + "%s %s %s" % (self._arg_name, " ".join(self._args), " ".join(args))
            return commands.getoutput(cmd)


class ShellOutCommand(object):
    
    _soa = ShellOutArg

    def __init__(self, cmd):
        self._cmd = cmd

    def __getattr__(self, x):
        return self._soa(self._cmd, x)

    def __call__(self, *args):
        import commands

        to_run = self._cmd + " " + " ".join(args)
        return commands.getoutput(to_run)


class ShellOutModule(object):

    def __init__(self):
        self._soc = ShellOutCommand
        self._soa = ShellOutArg

    def __getattr__(self, x):
        return self._soc(x)


import sys
sys.modules[__name__] = ShellOutModule()
