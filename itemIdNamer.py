#!/usr/bin/env python3

"""
Python 3.6.x

Very simply takes in a file, reads all integer literals
from the file, and emits a .txt file that contains the names
of the items whose IDs correspond to the integer literals
in the original file.

Must be placed in /wz folder with access to /wz/String.wz/
"""

import re

numre = re.compile(r'[0-9]+')
xmlentities = {
    '&': "&amp;",
    "'": "&apos;",
    '>': "&gt;",
    '<': "&lt;",
    '"': "&quot;",
}

filename = input("File name: ")
itemcache = {}
ids = []
out = ""


def xmlunescape(string):
    for char, entity in xmlentities.items():
        string = string.replace(entity, char)
    return string


with open(filename, "r", encoding="utf8") as f:
    ids = map(lambda ns: int(ns), numre.findall(f.read()))

for itemid in ids:
    if itemid in itemcache:
        itemname = itemcache[itemid]
    else:
        itemstringpath = "String.wz/"
        if itemid // 1000000 == 1:    # Equip
            itemstringpath += "Eqp.img.xml"
        elif itemid // 1000000 == 4:  # Etc
            itemstringpath += "Etc.img.xml"
        elif itemid // 1000000 == 2:  # Use
            itemstringpath += "Consume.img.xml"
        elif itemid // 1000000 == 3:  # Setup
            itemstringpath += "Ins.img.xml"
        elif itemid // 1000000 == 5:  # Cash
            itemstringpath += "Cash.img.xml"
        else:
            raise Exception("Unrecognized item type: " + str(itemid))

        with open(itemstringpath, encoding="utf8") as itemstring:
            pattern = r'(?<=name="' + str(itemid) + \
                r'">)(<string name="desc" value="[^"]+"/>)?' + \
                r'(<string name="name" value=")([^"]+)'
            itemnamematch = re.search(pattern, itemstring.read())
            if itemnamematch:
                itemname = xmlunescape(itemnamematch.groups()[-1].strip())
                itemcache[itemid] = itemname
            else:
                raise Exception(
                    "Could not find item name for itemid " + str(itemid))
    out += itemname + "\n"

with open(filename + ".txt", "w", encoding="utf8") as f:
    f.write(out)
