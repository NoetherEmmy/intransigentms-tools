#!/usr/bin/env python3

"""
Python 3.x.x

Concatenates multiple .sql files (specifically,
the results of multiple applications of
dropTableGenerator_.py) into a single master
query.
"""

from os import listdir

concat = \
    "INSERT INTO monsterdrops\n" + \
    "(monsterid, itemid, chance)\n" + \
    "VALUES\n"
i = 0

for file in listdir("./"):
    if not file.endswith(".sql"):
        continue

    i += 1
    with open(file, "r", encoding="utf8") as f:
        concat += f.read()

with open("droptable_.sql", "w", encoding="utf8") as f:
    f.write(concat)

print(str(i))
