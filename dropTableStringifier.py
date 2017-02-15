#!/usr/bin/env python3

"""
Python 3.6.x

This script is used to convert an *.sql file containing a single
``INSERT INTO`` query — used to insert entires into the
drop table — into Markdown format.

The lines of the *.sql file containing the actual data (this script
ignores lines that are used for things like ``INSERT INTO``)
must be of the form::

    (1234567, 7654321, 650), -- Comments are optional.

where the first integer is the mob ID, followed by the item ID,
followed by the chance.

This is the style used by other tools here,
like the dropTableGenerator.py or randomDropTabler.py.

I use this for adding new drop info to patch notes.
"""

import re

inputfile = input("Enter the filepath of the SQL query file: ")
outputfile = inputfile + ".md"
mobcache = {}
itemcache = {}
nnmatch = re.compile(r'[0-9]+')
out = ""
xmlentities = {
    '&': "&amp;",
    "'": "&apos;",
    '>': "&gt;",
    '<': "&lt;",
    '"': "&quot;",
}


def xmlunescape(string):
    for char, entity in xmlentities.items():
        string = string.replace(entity, char)
    return string


nums = []
with open(inputfile, "r", encoding="utf8") as f:
    fcontents = map(lambda l: l[:l.find("--")], f.readlines())
    nums = list(map(lambda s: int(s), nnmatch.findall("\n".join(fcontents))))

if len(nums) % 3 != 0:
    raise Exception(
        "Malformed input; " +
        "number of values is not a multiple of 3. " +
        "Input should be in a series of 3-tuples of natural numbers.")

i = 0
for num in nums:
    if i > 2:
        i -= 3
    if i == 0:    # monsterid
        out += "* "
        if num in mobcache:
            mobname = mobcache[num]
        else:
            with open("String.wz/Mob.img.xml", encoding="utf8") as mobstring:
                pattern = r'(?<=name="' + str(num) + \
                    r'"><string name="name" value=")[^"]+'
                mobnamematch = re.search(
                    pattern, mobstring.read())
                if mobnamematch:
                    mobname = mobnamematch.group()
                    mobcache[num] = mobname
                else:
                    raise Exception(
                        "Could not find mob name for mobid " + str(num))
        out += mobname
        if mobname[-1] == 's':
            out += "e"
        out += "s now drop "
    elif i == 1:  # itemid
        if num in itemcache:
            itemname = itemcache[num]
        else:
            itemstringpath = "String.wz/"
            if num // 1000000 == 1:    # Equip
                itemstringpath += "Eqp.img.xml"
            elif num // 1000000 == 4:  # Etc
                itemstringpath += "Etc.img.xml"
            elif num // 1000000 == 2:  # Use
                itemstringpath += "Consume.img.xml"
            elif num // 1000000 == 3:  # Setup
                itemstringpath += "Ins.img.xml"
            elif num // 1000000 == 5:  # Cash
                itemstringpath += "Cash.img.xml"
            else:
                raise Exception("Unrecognized item type: " + str(num))

            with open(itemstringpath, encoding="utf8") as itemstring:
                pattern = r'(?<=name="' + str(num) + \
                    r'">)(<string name="desc" value="[^"]+"/>)?' + \
                    r'(<string name="name" value=")([^"]+)'
                itemnamematch = re.search(
                    pattern, itemstring.read())
                if itemnamematch:
                    itemname = xmlunescape(itemnamematch.groups()[-1].strip())
                    itemcache[num] = itemname
                else:
                    raise Exception(
                        "Could not find item name for itemid " + str(num))
        out += itemname
        if itemname[-1] == 's' and itemname[-2] != 'e' and itemname[-2] != 'g':
            out += "e"
        if itemname[-1] == 'x':
            out += "e"
        out += "s "
    elif i == 2:  # chance
        if num < 5:
            out += "100% of the time"
        elif num < 20:
            out += "very often"
        elif num < 100:
            out += "somewhat often"
        elif num < 400:
            out += "every once in a while"
        elif num < 4000:
            out += "very occasionally"
        elif num < 12000:
            out += "rarely"
        else:
            out += "with extreme rarity"
        out += ".\n"
    i += 1

with open(outputfile, "w", encoding="utf8") as f:
    f.write(out)
