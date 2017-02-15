#!/usr/bin/env python

"""
Any version of Python

Takes in the first gachapon NPC script (ID 9100100) and creates
a new gachapon NPC script (named newgach.js) that is identical,
except that all instances of ``cm.gainItem()`` have two additional
arguments passed in, ``true`` and ``true``.

This will make the gachapon randomize item stats while still
displaying the items that are gained in the bottom right of the
user's screen.

Must be placed in NPC script folder.
"""

lines = []

with open("9100100.js", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "cm.gainItem(" in lines[i]:
        splitted = lines[i].split(")")
        if len(splitted) != 2:
            raise ValueError(
                "Line with 'cm.gainItem(' has multiple right parentheses.")
        splitted[0] += ", true, true)"
        lines[i] = splitted[0] + splitted[1]

with open("newgach.js", "w") as f:
    f.writelines(lines)
