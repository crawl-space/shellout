.. image:: https://img.shields.io/pypi/v/shellout.svg
    :target: https://crate.io/packages/shellout/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/shellout.svg
    :target: https://crate.io/packages/shellout/
    :alt: Number of PyPI downloads

.. image:: http://b.repl.ca/v1/license-MIT-orange.png
    :target: COPYING
    :alt: MIT License

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
