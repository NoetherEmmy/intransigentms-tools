#!/usr/bin/env python3

"""
Python 3.x.x

Used inside of a folder of quest .ini files
(see `https://github.com/NoetherEmmy/intransigentms-quests`_)
to change the EXP that they award by some factor.
"""

from os import listdir

factor = float(input("Factor to multiply all EXP rewards by: "))

for filename in listdir():
    if filename[-4:] == ".ini":
        lines = []
        with open(filename.split("\\/")[-1], "r") as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if "EXP=" in line:
                newnumber = str(int(line[line.find("=") + 1:]) * factor)
                lines[i] = line[:line.find("=") + 1] + newnumber + "\n"
                break

        with open(filename.split("\\/")[-1], "w") as f:
            f.writelines(lines)
