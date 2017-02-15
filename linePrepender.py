#!/usr/bin/env python

"""
Any version of Python

For people using repacks built on Java 7 or earlier,
their scripts are likely interpreted using Rhino.

Java 8+ brings us a new Javascript engine, Nashorn.

This script is one of two scripts
(the other being packageFixer.py)
that can be run on the old scripts in order to make
them function with Nashorn.

Must be run from the root directory of the server with
access to /scripts/.

NOTE: This is a bandaid fix, old scripts should be
further assimilated into Nashorn's style once they are
minimally working, e.g. use ``Java.type()`` for imports.
"""

import os


def lineprepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + '\n' + content)


for dirpath, dirnames, filenames in os.walk("./scripts"):
    for file in filenames:
        if file[len(file) - 3:] == ".js":
            lineprepender(os.path.join(dirpath, file),
                          "load('nashorn:mozilla_compat.js');")
