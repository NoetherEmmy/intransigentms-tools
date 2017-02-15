#!/usr/bin/env python3

"""
Python 3.6.x

Aggregates and ranks the EXP/HP ratio for mobs of a
specified type (boss, nonboss, or both) within a given
level range, and prints them out in sorted order with
the best ratios at the bottom.

Must be placed in /wz/.
"""

import re
from os import listdir

levelre = re.compile(r'<int name="level" value="([0-9]+)"')
hpre = re.compile(r'<int name="maxHP" value="([0-9]+)"')
hprealt = re.compile(r'<string name="maxHP" value="([0-9]+)"')
watkre = re.compile(r'<int name="PADamage" value="([0-9]+)"')
matkre = re.compile(r'<int name="MADamage" value="([0-9]+)"')
expre = re.compile(r'<int name="exp" value="([0-9]+)"')
bossre = re.compile(r'<int name="boss" value="([0-9]+)"')
namerestart = r'<imgdir name="'
namereend = r'"><string name="name" value="([^"]+)"'
bossfilter = int(
    input("0 to show only nonboss mobs, 1 for boss, or 2 for both: "))
levelrange = input("Level range, in \"x - y\" form: ")
levelrangesplit = levelrange.split('-')
minlv = int(levelrangesplit[0].strip())
maxlv = int(levelrangesplit[1].strip())
mobs = []
stringcontent = ""
out = ""

for file in listdir("./Mob.wz"):
    if not file.endswith(".img.xml"):
        continue
    if "9999999" in file:
        continue
    content = ""
    with open("./Mob.wz/" + file, "r", encoding="utf8") as f:
        content = f.read()

    try:
        level = levelre.search(content).group(1)
        hpmatch = hpre.search(content)
        if not hpmatch:
            hpmatch = hprealt.search(content)
        hp = "0"
        if hpmatch:
            hp = hpmatch.group(1)
        watk = watkre.search(content).group(1)
        matk = matkre.search(content).group(1)
        expmatch = expre.search(content)
        exp = "0"
        if expmatch:
            exp = expmatch.group(1)
    except AttributeError as ae:
        raise AttributeError(file + ": " + str(ae))
    boss = bossre.search(content)
    isboss = False
    if boss:
        isboss = int(bossre.search(content).group(1)) > 0

    if bossfilter == 0 and isboss:
        continue
    if bossfilter == 1 and not isboss:
        continue
    if int(level) < minlv:
        continue
    if int(level) > maxlv:
        continue

    if stringcontent == "":
        with open("./String.wz/Mob.img.xml", "r", encoding="utf8") as f:
            stringcontent = f.read()

    mobid = int(file[:-8])
    name = re.search(
        namerestart + str(mobid) + namereend, stringcontent).group(1)

    xphpratio = float(exp) / float(hp)
    mobs.append((name, mobid, xphpratio, level, exp, hp, watk, matk, isboss))

for m in sorted(mobs, key=lambda m: m[2]):
    out = m[0] + " (" + str(m[1]) + "), XP/HP ratio: " + str(m[2]) + \
        ", level: " + m[3] + ", EXP: " + m[4] + ", HP: " + m[5] + \
        ", watk: " + m[6] + ", matk: " + m[7] + ", is boss?: " + str(m[8])
    print(out)
