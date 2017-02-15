#!/usr/bin/env python3

"""
Python 3.6.x

Takes in a list of mob IDs and outputs a neatly-formatted
list of stats for all of the mobs.

Should be placed in /wz/ with access to /wz/String.wz/
and /wz/Mob.wz/
"""

import re

levelre = re.compile(r'<int name="level" value="([0-9]+)"')
hpre = re.compile(r'<int name="maxHP" value="([0-9]+)"')
watkre = re.compile(r'<int name="PADamage" value="([0-9]+)"')
matkre = re.compile(r'<int name="MADamage" value="([0-9]+)"')
wdefre = re.compile(r'<int name="PDDamage" value="([0-9]+)"')
mdefre = re.compile(r'<int name="MDDamage" value="([0-9]+)"')
accre = re.compile(r'<int name="acc" value="([0-9]+)"')
avoidre = re.compile(r'<int name="eva" value="([0-9]+)"')
expre = re.compile(r'<int name="exp" value="([0-9]+)"')
bossre = re.compile(r'<int name="boss" value="([0-9]+)"')
namerestart = r'<imgdir name="'
namereend = r'"><string name="name" value="([^"]+)"'
out = ""

mobids = []
mobidfile = input("File containing mob IDs: ")
mobidre = re.compile(r'[0-9]{6,7}')
with open(mobidfile, "r", encoding="utf8") as f:
    mobids = map(lambda s: int(s), mobidre.findall(f.read()))

for mobid in mobids:
    content = ""
    with open("Mob.wz/" + str(mobid) + ".img.xml", "r", encoding="utf8") as f:
        content = f.read()

    level = levelre.search(content).group(1)
    hp = hpre.search(content).group(1)
    watk = watkre.search(content).group(1)
    matk = matkre.search(content).group(1)
    wdef = wdefre.search(content).group(1)
    mdef = mdefre.search(content).group(1)
    acc = accre.search(content).group(1)
    avoid = avoidre.search(content).group(1)
    exp = expre.search(content).group(1)
    boss = bossre.search(content)
    isboss = False
    if boss:
        isboss = int(bossre.search(content).group(1)) > 0

    with open("String.wz/Mob.img.xml", "r", encoding="utf8") as f:
        content = f.read()

    name = re.search(namerestart + str(mobid) + namereend, content).group(1)

    out += name
    out += " (" + str(mobid) + ")"
    out += "\n    "
    out += "Level: "
    out += level
    out += "\n    "
    out += "HP: "
    out += hp
    out += "\n    "
    out += "Weapon attack: "
    out += watk
    out += "\n    "
    out += "Magic attack: "
    out += matk
    out += "\n    "
    out += "Weapon defense: "
    out += wdef
    out += "\n    "
    out += "Magic defense: "
    out += mdef
    out += "\n    "
    out += "Accuracy: "
    out += acc
    out += "\n    "
    out += "Avoidability: "
    out += avoid
    out += "\n    "
    out += "Exp: "
    out += exp
    out += "\n    "
    out += "Boss?: "
    out += str(isboss)
    out += "\n\n"

with open("mob-stats.txt", "w", encoding="utf8") as o:
    o.write(out)
