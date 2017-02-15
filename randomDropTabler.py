#!/usr/bin/env python

"""
Python 2.7.x

Given access to a full /wz/ directory and a file (inputted
during execution of the script) containing mob IDs,
this script generates drop tables for all the mobs with
the IDs given by the file, randomly.
"""

from __future__ import division, print_function
from codecs import open as o
import re
import os
import random

"""
mobinput = raw_input("List of comma-separated mob IDs: ")
mobids = [idstr.strip() for idstr in mobinput.split(',')]
"""
mobinput = raw_input("Mob IDs file: ")
mobids = []
with o(mobinput, "r", "utf-8") as f:
    mobids.extend(re.findall(r'[0-9]{7}', f.read()))

stimre = re.compile(r'<imgdir name="0(413[0-9]{4})">')
materialre1 = re.compile(r'<imgdir name="0(401[0-9]{4})">')
materialre2 = re.compile(r'<imgdir name="0(402[0-9]{4})">')
bulletre = re.compile(r'<imgdir name="0(233[0-9]{4})">')
throwingstarre = re.compile(r'<imgdir name="0(207[0-9]{4})">')
masterybookre = re.compile(r'<imgdir name="0(229[0-9]{4})">')
curativere = re.compile(r'<imgdir name="0(205[0-9]{4})">')
scrollre = re.compile(r'<imgdir name="0(204[0-9]{4})">')
successre = re.compile(r'<int name="success" value="([0-9]+)"')
legalsuccessrates = ["10", "30", "60", "70"]
potionre1 = re.compile(r'<imgdir name="0(202[0-9]{4})">')
potionre2 = re.compile(r'<imgdir name="0(200[0-9]{4})">')
cashre = re.compile(r'<int name="cash" value="1"')
questre = re.compile(r'<int name="quest" value="1"')
tradeblockre = re.compile(r'<int name="tradeBlock" value="1"')
equiplevelre = re.compile(r'<int name="reqLevel" value="([0-9]+)"')
equiplevelaltre = re.compile(r'<string name="reqLevel" value="([0-9]+)"')
moblevelre = re.compile(r'<int name="level" value="([0-9]+)"')
bossre = re.compile(r'<int name="boss" value="([0-9]+)"')
stringlocaterestart = r'<imgdir name="'
stringlocatereend = r'">'
namere = re.compile(r'<string name="name" value="([^"]+)"')

stimdata = []
materialdata = []
oredata = []
refineddata = []
projectiledata = []
masterybookdata = []
curativedata = []
scrolldata = []
potiondata = []
equipdata = []
chaosscroll = u"2049100"
innoscroll = u"2049004"
cog = u"2049122"
cleanslates = [u"2049000", u"2049001", u"2049002", u"2049003"]
equiptypes = [u"Cap", u"Cape", u"Coat", u"Glove", u"Longcoat",
              u"Pants", u"Shield", u"Shoes", u"Weapon"]
xmlentities = {
    "&amp;": '&',
    "&apos;": "'",
    "&gt;": '>',
    "&lt;": '<',
    "&quot;": '"',
}
etcstring = ""
consumestring = ""
equipstring = ""
out = ""


def remove(list_, object_):
    try:
        list_.remove(object_)
    except ValueError:
        pass


def xmlunescape(string):
    for entity, char in xmlentities.iteritems():
        string = string.replace(entity, char)
    return string


with o("./Item.wz/Etc/0413.img.xml", "r", "utf-8") as f:
    stimdata.extend(stimre.findall(f.read()))

with o("./Item.wz/Etc/0401.img.xml", "r", "utf-8") as f:
    materialdata.extend(materialre1.findall(f.read()))

with o("./Item.wz/Etc/0402.img.xml", "r", "utf-8") as f:
    materialdata.extend(materialre2.findall(f.read()))

oredata = [ore for ore in materialdata if int(ore) // 1000 % 10 == 0]
refineddata = [
    refined for refined in materialdata if int(refined) // 1000 % 10 == 1]

with o("./Item.wz/Consume/0233.img.xml", "r", "utf-8") as f:
    projectiledata.extend(bulletre.findall(f.read()))

with o("./Item.wz/Consume/0207.img.xml", "r", "utf-8") as f:
    projectiledata.extend(throwingstarre.findall(f.read()))

remove(projectiledata, u"2070014")  # Devil Rain Throwing Star
remove(projectiledata, u"2070018")  # Balanced Fury
remove(projectiledata, u"2330005")  # Eternal Bullet
remove(projectiledata, u"2070016")  # Crystal Ilbi Throwing Stars
remove(projectiledata, u"2330006")  # Bullet for Novice Pirates
remove(projectiledata, u"2070015")  # A Beginner Thief's Throwing Stars

with o("./Item.wz/Consume/0229.img.xml", "r", "utf-8") as f:
    masterybookdata.extend(masterybookre.findall(f.read()))

with o("./Item.wz/Consume/0205.img.xml", "r", "utf-8") as f:
    curativedata.extend(curativere.findall(f.read()))

remove(curativedata, u"2050099")  # Flaming feather
remove(curativedata, u"2050098")  # The Lost Eye
remove(curativedata, u"2050005")  # One View

with o("./Item.wz/Consume/0204.img.xml", "r", "utf-8") as f:
    scrollcontents = f.read()
    scrolliter = scrollre.finditer(scrollcontents)
    for scrollmatch in scrolliter:
        successmatch = successre.search(scrollcontents, scrollmatch.start())
        if successmatch:
            success = successmatch.group(1)
            if success not in legalsuccessrates:
                continue
        else:
            raise RuntimeError(
                "Could not find success rate for " + scrollmatch.group(1))
        scrolldata.append(scrollmatch.group(1))

remove(scrolldata, chaosscroll)
remove(scrolldata, innoscroll)

with o("./Item.wz/Consume/0202.img.xml", "r", "utf-8") as f:
    potiondata.extend(potionre1.findall(f.read()))

with o("./Item.wz/Consume/0200.img.xml", "r", "utf-8") as f:
    potiondata.extend(potionre2.findall(f.read()))

remove(potiondata, u"2000013")  # Red Potion for Beginners
remove(potiondata, u"2000014")  # Blue Potion for Beginners
remove(potiondata, u"2000015")  # Orange Potion for Beginners
remove(potiondata, u"2022121")  # Gelt Chocolate
remove(potiondata, u"2022282")  # Naricain's Demon Elixir
remove(potiondata, u"2000015")  # Onyx Apple
remove(potiondata, u"2022108")  # Horntail Squad: Victory
remove(potiondata, u"2022283")  # Subani's Mystic Cauldron
remove(potiondata, u"2022273")  # Ssiws Cheese
remove(potiondata, u"2022251")  # Maple Pop
remove(potiondata, u"2022338")  # VitroJuice
remove(potiondata, u"2022339")  # NitroJuice
remove(potiondata, u"2022340")  # BlastroJuice
remove(potiondata, u"2022341")  # ElectroJuice
remove(potiondata, u"2022342")  # MegaJuice
remove(potiondata, u"2022343")  # GigaJuice
remove(potiondata, u"2022344")  # JigaJuice
remove(potiondata, u"2022117")  # Maple Syrup
remove(potiondata, u"2022118")  # Admin's Congrats
remove(potiondata, u"2022070")  # Congrats from GM
remove(potiondata, u"2022303")  # MISSINGNO
remove(potiondata, u"2022196")  # Wedding Bouquet

for equiptype in equiptypes:
    for filename in os.listdir("./Character.wz/" + equiptype):
        xmlname = "./Character.wz/" + equiptype + "/" + filename
        with o(xmlname, "r", "utf-8") as f:
            contents = f.read()
            cashmatch = cashre.search(contents)
            if cashmatch:
                continue
            questmatch = questre.search(contents)
            if questmatch:
                continue
            tradeblockmatch = tradeblockre.search(contents)
            if tradeblockmatch:
                continue
            equiplevelmatch = equiplevelre.search(contents)
            reqlevel = -1
            if equiplevelmatch:
                reqlevel = int(equiplevelmatch.group(1))
            else:
                equiplevelmatch = equiplevelaltre.search(contents)
                if equiplevelmatch:
                    reqlevel = int(equiplevelmatch.group(1))
                else:
                    print("Could not find req. level for " + filename[1:-8])
            equipdata.append((filename[1:-8], reqlevel))

remove(equipdata, (u"1002357", 50))  # Zakum Helmet (1)
remove(equipdata, (u"1002390", 50))  # Zakum Helmet (2)
remove(equipdata, (u"1002430", 60))  # Zakum Helmet (3)
remove(equipdata, (u"1002858", 100))  # Chaos Zakum Helmet

with o("./String.wz/Etc.img.xml", "r", "utf-8") as f:
    etcstring = f.read()

with o("./String.wz/Consume.img.xml", "r", "utf-8") as f:
    consumestring = f.read()

with o("./String.wz/Eqp.img.xml", "r", "utf-8") as f:
    equipstring = f.read()

for mobid in mobids:
    mobcontent = ""
    with o("./Mob.wz/" + mobid.zfill(7) + ".img.xml", "r", "utf-8") as f:
        mobcontent = f.read()

    level = int(moblevelre.search(mobcontent).group(1))
    boss = bossre.search(mobcontent)
    isboss = False
    if boss:
        isboss = int(bossre.search(mobcontent).group(1)) > 0

    if random.randint(0, 1) == 0:
        """ Stims """
        stims = set()
        stimcount = random.randint(1, 3)
        for i in xrange(stimcount):
            stims.add(random.choice(stimdata))
        for stim in stims:
            idmatch = re.search(stringlocaterestart +
                                stim + stringlocatereend, etcstring)
            namematch = namere.search(etcstring, idmatch.start())
            if namematch:
                name = namematch.group(1)
            else:
                raise RuntimeError("Cannot find name for stim " +
                                   stim + ", idmatch.start(): " +
                                   str(idmatch.start()))
            out += "("
            out += mobid
            out += ", "
            out += stim
            out += ", "
            out += "555), -- "
            out += xmlunescape(name.strip())
            out += "\n"

    """ Materials """
    materials = set()
    materialscount = random.randint(2, 8)
    for i in xrange(materialscount):
        if isboss:
            materials.add(random.choice(refineddata))
        else:
            materials.add(random.choice(oredata))
    for material in materials:
        idmatch = re.search(stringlocaterestart +
                            material + stringlocatereend, etcstring)
        namematch = namere.search(etcstring, idmatch.start())
        if namematch:
            name = namematch.group(1)
        else:
            raise RuntimeError("Cannot find name for material " + material)
        out += "("
        out += mobid
        out += ", "
        out += material
        out += ", "
        out += "240), -- "
        out += xmlunescape(name.strip())
        out += "\n"

    """ Projectiles """
    projectiles = set()
    projectilescount = random.randint(0, 2)
    for i in xrange(projectilescount):
        projectiles.add(random.choice(projectiledata))
    for projectile in projectiles:
        idmatch = re.search(stringlocaterestart +
                            projectile + stringlocatereend, consumestring)
        if not idmatch:
            raise RuntimeError(
                "Cannot find ID in string data for " + projectile)
        name = namere.search(consumestring, idmatch.start()).group(1)
        out += "("
        out += mobid
        out += ", "
        out += projectile
        out += ", "
        out += "850), -- "
        out += xmlunescape(name.strip())
        out += "\n"

    if level > 85:
        """ Mastery books """
        masterybooks = set()
        masterybookcount = random.randint(0, 3)
        for i in xrange(masterybookcount):
            masterybooks.add(random.choice(masterybookdata))
        for masterybook in masterybooks:
            idmatch = re.search(stringlocaterestart +
                                masterybook + stringlocatereend, consumestring)
            if not idmatch:
                raise RuntimeError(
                    "Cannot find ID in string data for " + masterybook)
            name = namere.search(consumestring, idmatch.start()).group(1)
            out += "("
            out += mobid
            out += ", "
            out += masterybook
            out += ", "
            out += "10000), -- "
            out += xmlunescape(name.strip())
            out += "\n"

    if random.randint(0, 1) == 0:
        """ Curatives """
        curatives = set()
        curativescount = random.randint(1, 2)
        for i in xrange(curativescount):
            curatives.add(random.choice(curativedata))
        for curative in curatives:
            idmatch = re.search(stringlocaterestart +
                                curative + stringlocatereend, consumestring)
            if not idmatch:
                raise RuntimeError(
                    "Cannot find ID in string data for " + curative)
            name = namere.search(consumestring, idmatch.start()).group(1)
            out += "("
            out += mobid
            out += ", "
            out += curative
            out += ", "
            out += "330), -- "
            out += xmlunescape(name.strip())
            out += "\n"

    """ Scrolls """
    scrolls = set()
    scrollscount = random.randint(3, 16)
    for i in xrange(scrollscount):
        if random.randint(0, 230) == 22:
            chance = 30000
            if isboss:
                chance = 300
            scrolls.add((chaosscroll, chance))
            continue
        if random.randint(0, 330) == 3:
            chance = 50000
            if isboss:
                chance = 500
            scrolls.add((cog, chance))
            continue
        if random.randint(0, 180) == 37:
            chance = 20000
            if isboss:
                chance = 200
            scrolls.add((innoscroll, chance))
            continue
        if random.randint(0, 125) == 19:
            cleanslate = random.choice(cleanslates)
            chance = 3000
            if isboss:
                chance = 45
            scrolls.add((cleanslate, chance))
            continue
        chance = 850
        if isboss:
            chance = 85
        scrolls.add((random.choice(scrolldata), chance))
    for scroll in scrolls:
        idmatch = re.search(stringlocaterestart +
                            scroll[0] + stringlocatereend, consumestring)
        if not idmatch:
            raise RuntimeError(
                "Cannot find ID in string data for " + scroll[0])
        name = namere.search(consumestring, idmatch.start()).group(1)
        out += "("
        out += mobid
        out += ", "
        out += scroll[0]
        out += ", "
        out += str(scroll[1])
        out += "), -- "
        out += xmlunescape(name.strip())
        out += "\n"

    """ Potions """
    potions = set()
    potionscount = random.randint(1, 4)
    for i in xrange(potionscount):
        potions.add(random.choice(potiondata))
    for potion in potions:
        idmatch = re.search(stringlocaterestart +
                            potion + stringlocatereend, consumestring)
        if not idmatch:
            raise RuntimeError(
                "Cannot find ID in string data for " + potion)
        name = namere.search(consumestring, idmatch.start()).group(1)
        out += "("
        out += mobid
        out += ", "
        out += potion
        out += ", "
        out += "350), -- "
        out += xmlunescape(name.strip())
        out += "\n"

    """ Equipment """
    equips = set()
    equipscount = random.randint(13, 30)
    lowerlevelbound = min(3 * level / 4, 90)
    upperlevelbound = 11 * level / 10
    localequipdata = [equip[0] for equip in equipdata
                      if equip[1] >= lowerlevelbound and
                      equip[1] <= upperlevelbound or
                      equip[1] < 0]
    for i in xrange(equipscount):
        equips.add(random.choice(localequipdata))
    for equip in equips:
        idmatch = re.search(stringlocaterestart +
                            equip + stringlocatereend, equipstring)
        name = namere.search(equipstring, idmatch.start()).group(1)
        out += "("
        out += mobid
        out += ", "
        out += equip
        out += ", "
        out += "650), -- "
        out += xmlunescape(name.strip())
        out += "\n"

    out += "\n"

i = 0
while os.path.isfile("random-drop-table" + str(i).zfill(4) + ".sql"):
    i += 1

with o("random-drop-table" + str(i).zfill(4) + ".sql", "w", "utf-8") as f:
    f.write(out)
