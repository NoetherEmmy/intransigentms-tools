# This script runs through a text file containing lines from any GM Handbook *.txt(s)
# as well as potentially some headers and empty lines (lines that don't have an integer as the)
# second word on the line are ignored). It puts all items into a JavaScript array,
# to be sold by Mia as cash items, with the prices pre-set by item type.
# The file name is specified in the code itself, in the variable "filename".

import math

filename = "newNx.txt"
items = []

with open(filename, "r") as f:
    lines = f.readlines()
    for line in lines:
        splitted = line.split()
        if len(splitted) > 1:
            try:
                newitem = []
                foo = int(splitted[1])
                if splitted[2][0] == "(":
                    newitem.append(splitted[2].strip("()"))
                    name = ""
                    for i in range(4, len(splitted)):
                        if i != len(splitted) - 1:
                            name += splitted[i] + " "
                        else:
                            name += splitted[i]
                    newitem.append(name)
                else:
                    newitem.append(splitted[1])
                    name = ""
                    for i in range(3, len(splitted)):
                        if i != len(splitted) - 1:
                            name += splitted[i] + " "
                        else:
                            name += splitted[i]
                    newitem.append(name)
                items.append(newitem)
            except:
                continue

items.sort(key=lambda x: x[0])

out = "["
for item in items:
    itemid = int(item[0])
    itemtype = int(math.floor(float(itemid) / 10000.0))
    itemprice = 3000
    if itemtype == 100: # hats
        itemprice = 2700
    elif itemtype == 170: # weapons
        itemprice = 3000
    elif itemtype == 110: # capes
        itemprice = 2000
    elif itemtype == 105: # overalls
        itemprice = 3000
    elif itemtype == 190: # mounts
        itemprice = 6000
    elif itemtype == 500: # pets
        itemprice = 7700
    out += "[" + item[0] + ", \"" + item[1] + "\", " + str(itemprice) + "], "

with open("nxitems.txt", "w") as f:
    f.write(out)
