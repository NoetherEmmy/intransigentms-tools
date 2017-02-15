#!/usr/bin/env python3

"""
Python 3.6.x

This program takes any number of map XML files
and prints out their dependencies in a new *.txt file.

Keep in mind that each dependency may have multiple parts,
e.g. a mob needs its mob file as well as string and sound,
and UI in the case of bosses with fullscreen HP bars.

The main dependencies file emitted by this script contains
all the info for each map in one place, while all the other
files emitted consolidate the resources needed for all the
maps inputted all together, sorted, with no duplicates.

Requires:
    xmltodict (to install: ``pip install xmltodict``)
"""

import tkinter as tk
from tkinter import filedialog
import xmltodict


def isIntegral(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


root = tk.Tk()
root.withdraw()
filepaths = filedialog.askopenfilenames(filetypes=[("XML files", ".xml")],
                                        title="Select the dumped " +
                                        "<mapid>.img.xml files you'd " +
                                        "like to check for dependencies:")
thisdir = ""
backset = set()
mobset = set()
npcset = set()
tilesetset = {}
objsetset = {}
bgmset = set()
mapmarkset = set()

for filepath in filepaths:
    fp = open(filepath, "r", encoding="utf8")
    img = xmltodict.parse(fp.read())
    fp.close()

    bgm = "N/A"
    mapmark = "N/A"
    back = []
    mobs = []
    npcs = []
    tilesets = {}
    objsets = {}

    try:
        for imgdir in img["imgdir"]["imgdir"]:
            try:
                if imgdir["@name"] == "info":
                    for infostring in imgdir["string"]:
                        if infostring["@name"] == "bgm":
                            bgm = infostring["@value"]
                        elif infostring["@name"] == "mapMark":
                            mapmark = infostring["@value"]
                elif imgdir["@name"] == "back":
                    for backimgdir in imgdir["imgdir"]:
                        if backimgdir["string"]["@value"] not in back:
                            back.append(backimgdir["string"]["@value"])
                elif imgdir["@name"] == "life":
                    try:
                        temp = imgdir["imgdir"][0]["string"]
                        for lifeimgdir in imgdir["imgdir"]:
                            lifetype = ""
                            lifeid = ""
                            for lifestring in lifeimgdir["string"]:
                                if lifestring["@name"] == "type":
                                    lifetype = lifestring["@value"]
                                elif lifestring["@name"] == "id":
                                    lifeid = lifestring["@value"]
                            if lifetype == "m":
                                if lifeid not in mobs:
                                    mobs.append(lifeid)
                            elif lifetype == "n":
                                if lifeid not in npcs:
                                    npcs.append(lifeid)
                            else:
                                raise ValueError(
                                    "life type is neither \"m\" nor \"n\"")
                    except:
                        if "imgdir" in imgdir:
                            lifeimgdir = imgdir["imgdir"]
                        else:
                            continue
                        lifetype = ""
                        lifeid = ""
                        for lifestring in lifeimgdir["string"]:
                            if lifestring["@name"] == "type":
                                lifetype = lifestring["@value"]
                            elif lifestring["@name"] == "id":
                                lifeid = lifestring["@value"]
                        if lifetype == "m":
                            if lifeid not in mobs:
                                mobs.append(lifeid)
                        elif lifetype == "n":
                            if lifeid not in npcs:
                                npcs.append(lifeid)
                        else:
                            raise ValueError(
                                "life type is neither \"m\" nor \"n\"")
                elif isIntegral(imgdir["@name"]):
                    currenttileset = ""
                    for intimgdir in imgdir["imgdir"]:
                        if intimgdir["@name"] == "info" and len(intimgdir) > 1:
                            try:
                                currenttileset = intimgdir["string"]["@value"]
                            except:
                                raise TypeError(
                                    "More than one string value under" +
                                    " info section of numbered node")
                            break
                    for intimgdir in imgdir["imgdir"]:
                        intimgdirlen = len(intimgdir)
                        if intimgdir["@name"] == "tile" and len(intimgdir) > 1:
                            for tileimgdir in intimgdir["imgdir"]:
                                if currenttileset in tilesets.keys():
                                    t = tilesets[currenttileset]
                                    if tileimgdir["string"]["@value"] not in t:
                                        tilesets[currenttileset].append(
                                            tileimgdir["string"]["@value"])
                                else:
                                    newtileset = []
                                    newtileset.append(
                                        tileimgdir["string"]["@value"])
                                    tilesets[currenttileset] = newtileset
                        elif intimgdir["@name"] == "obj" and intimgdirlen > 1:
                            for objimgdir in intimgdir["imgdir"]:
                                currentobjset = ""
                                l0 = ""
                                l1 = ""
                                l2 = ""
                                try:
                                    for objstring in objimgdir["string"]:
                                        if objstring["@name"] == "oS":
                                            currentobjset = objstring["@value"]
                                        elif objstring["@name"] == "l0":
                                            l0 = objstring["@value"]
                                        elif objstring["@name"] == "l1":
                                            l1 = objstring["@value"]
                                        elif objstring["@name"] == "l2":
                                            l2 = objstring["@value"]
                                except TypeError:
                                    print(objimgdir)
                                obj = l0 + "/" + l1 + "/" + l2
                                if currentobjset in objsets.keys():
                                    objsets[currentobjset].append(obj)
                                else:
                                    newobjset = []
                                    newobjset.append(obj)
                                    objsets[currentobjset] = newobjset
            except TypeError:
                continue
    except Exception as e:
        raise RuntimeError("Exception reading file " +
                           filepath + ": " + str(e))

    back.sort()
    mobs.sort()
    npcs.sort()
    for tileset in tilesets.keys():
        tilesets[tileset].sort()
    for objset in objsets.keys():
        objsets[objset].sort()

    backset.update(back)
    mobset.update(mobs)
    npcset.update(npcs)
    for tileset in tilesets.keys():
        if tileset in tilesetset:
            tilesetset[tileset].update(tilesets[tileset])
        else:
            tilesetset[tileset] = set(tilesets[tileset])
    for objset in objsets.keys():
        if objset in objsetset:
            objsetset[objset].update(objsets[objset])
        else:
            objsetset[objset] = set(objsets[objset])
    bgmset.add(bgm)
    mapmarkset.add(mapmark)

    output = filepath.split("/")[-1]
    output = output.split(".")[0] + ":\n"
    output += "    Background music: " + bgm + "\n\n"
    output += "    Map mark/icon: " + mapmark + "\n\n"
    output += "    Backgrounds:\n"
    for bg in back:
        output += "        " + bg + "\n"
    output += "\n    Mobs:\n"
    for mob in mobs:
        output += "        " + mob + "\n"
    output += "\n    NPCs:\n"
    for npc in npcs:
        output += "        " + npc + "\n"
    output += "\n    Tile sets:\n"
    for tileset in tilesets.keys():
        output += "        " + tileset + "\n"
        for tile in tilesets[tileset]:
            output += "            " + tile + "\n"
    output += "\n    Object sets:\n"
    for objset in objsets.keys():
        output += "        " + objset + "\n"
        for obj in objsets[objset]:
            output += "            " + obj + "\n"
    output += "\n\n"

    filenamelen = len(filepath.split("/")[-1])
    thisdir = filepath[:-1 * filenamelen]
    with open(thisdir + "/dependencies.txt", "a", encoding="utf8") as o:
        o.write(output)

with open(thisdir + "/backgrounds.txt", "w", encoding="utf8") as b:
    for bg in sorted(backset):
        b.write(bg)
        b.write("\n")

with open(thisdir + "/mobs.txt", "w", encoding="utf8") as m:
    for mob in sorted(mobset):
        m.write(mob)
        m.write("\n")

with open(thisdir + "/npcs.txt", "w", encoding="utf8") as n:
    for npc in sorted(npcset):
        n.write(npc)
        n.write("\n")

with open(thisdir + "/tiles.txt", "w", encoding="utf8") as t:
    for tileset in sorted(tilesetset.keys()):
        t.write(tileset)
        t.write("\n")
        for tile in sorted(tilesetset[tileset]):
            t.write("    ")
            t.write(tile)
            t.write("\n")

with open(thisdir + "/objects.txt", "w", encoding="utf8") as o:
    for objset in sorted(objsetset.keys()):
        o.write(objset)
        o.write("\n")
        for obj in sorted(objsetset[objset]):
            o.write("    ")
            o.write(obj)
            o.write("\n")

with open(thisdir + "/bgm.txt", "w", encoding="utf8") as b:
    for bgm in sorted(bgmset):
        b.write(bgm)
        b.write("\n")

with open(thisdir + "/mapmarks.txt", "w", encoding="utf8") as m:
    for mapmark in sorted(mapmarkset):
        m.write(mapmark)
        m.write("\n")
