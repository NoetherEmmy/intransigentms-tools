#!/usr/bin/env python3

"""
Python 3.x.x

Very simply takes in a *.csv and takes each line into a single
JavaScript- (or Python-) style array.

Useful for taking the output of an SQL query (for one column
typically) and using it for a script.
"""

filename = input(
    "Enter the file name (or relative/absolute path " +
    "if it's not in this directory) of the *.csv: ")

lines = []
string = "["
with open(filename, "r") as f:
    lines = f.readlines()
    for i in range(1, len(lines)):
        string += lines[i].strip()
        if (i < len(lines) - 1):
            string += ", "
        else:
            string += "];"

print(string)
