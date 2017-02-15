#!/usr/bin/env python3

"""
Python 3.x.x

Used when a stack trace is printed due to a fatal NPC script error.
Because the stack trace cannot always reflectively include
the filename of the script, this can be used to find the
offending script.
"""

import os
import re

linenumber = int(input("Line number the error occured on: "))
offendingsnippetre = re.compile(
    input("Offending code snippet that can be found on the line: "))

candidates = []
for file in os.listdir("npc"):
    if file.endswith(".js"):
        lines = []
        with open("npc/" + file, "r", encoding="utf8") as f:
            lines = f.readlines()
        if len(lines) >= linenumber:
            if offendingsnippetre.search(lines[linenumber - 1]):
                candidates.append(file)

print(candidates)
