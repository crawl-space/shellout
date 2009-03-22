#!/usr/bin/python

class ShellOutArg(object):

    def __init__(self, cmd_string, arg_name):
        self._cmd_string = cmd_string
        if len(arg_name) == 1:
            self._arg_name = " -" + arg_name
            self._longopt = False
        else:
            self._arg_name = " --" + arg_name
            self._longopt = True
        self._called = False

    def __getattr__(self, x):
        cmd = self._cmd_string + self._arg_name
        if len(self._args) > 0:
            if self._longopt:
                cmd += "="
            else:
                cmd += " "
            cmd += " ".join(['"%s"' % x for x in self._args])
       
        return self.__class__(cmd, x)

    def __call__(self, *args):
        if not self._called:
            self._args = args
            self._called = True
            return self
        else:
            import commands

            cmd = self._cmd_string + self._arg_name
            if len(self._args) > 0:
                if self._longopt:
                    cmd += "="
                else:
                    cmd += " "
                cmd += " ".join(['"%s"' % x for x in self._args])
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

        return commands.getoutput(to_run)


class ShellOutModule(object):

    def __init__(self):
        self._soc = ShellOutCommand
        self._soa = ShellOutArg

    def __getattr__(self, x):
        return self._soc(x)


import sys
sys.modules[__name__] = ShellOutModule()
