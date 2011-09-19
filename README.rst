``shellout`` provides an OO-like interface to running shell commands.

Usage
-----
::

    >>> import shellout as so
    >>> print so.echo("hello, world")
    ... 'hello, world'
    >>> print so.python.version()
    ... 'Python 2.7.1'
    >>> print so.ls.color["always"]("/")
    ... bin
    ... dev
    ... etc
    ... home
    ... lib
    ... opt
    ... proc
    ... root
    ... sbin
    ... sys
    ... tmp
    ... usr
    ... var
    >>> print so.echo('with "both" \'quotes\'')
    ... with "both" 'quotes'

Installation
------------

::

    $ pip install shellout
