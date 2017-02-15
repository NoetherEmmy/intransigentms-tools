#!/usr/bin/env python

"""
Any version of Python

Used when a stack trace is printed due to a fatal portal script error.

Because the stack trace does not reflectively include the filename of
the script, this can be used to find the offending script.
"""

from __future__ import print_function
import os

linenumber = int(input("Line number the error occured on: "))
offendingSnippet = input(
    "Offending code snippet that can be found on the line: ")

candidates = []

for file in os.listdir("portal"):
    if file.endswith(".js"):
        with open("portal/" + file, "r") as f:
            lines = f.readlines()
            if len(lines) >= linenumber:
                if offendingSnippet in lines[linenumber - 1]:
                    candidates.append(file)

print(candidates)
