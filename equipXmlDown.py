# This is used for downgrading equipment from higher (post-BB) versions to a style that old clients (like v62)
# can read. Checks for references what include a full path (e.g. Character/weapon/4424242.img/default/0/1) and
# forces them to use abbreviations (e.g. ../../default/0/1).
# Uses XMLs exported from HaRepacked as classic XML.
# Requires xmltodict:
#     $ pip install xmltodict

from collections import OrderedDict
import os
import tkinter as tk
from tkinter import filedialog
import xmltodict

root = tk.Tk()
root.withdraw()
filepaths = filedialog.askopenfilenames(filetypes=[("XML files", ".xml")], title="Select the dumped *.img.xml files you would like to be edited:")

for filepath in filepaths:
    fp = open(filepath)
    img = xmltodict.parse(fp.read())
    fp.close()

    imgdircount = len(img["imgdir"]["imgdir"])
    for index in range(imgdircount):
        if img["imgdir"]["imgdir"][index]["@name"] != "info":
            if type(img["imgdir"]["imgdir"][index]["imgdir"]) is list:
                sublistlength = len(img["imgdir"]["imgdir"][index]["imgdir"])
                for numberedsub in range(sublistlength):
                    numberedsubname = img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["@name"]
                    rawsources = []
                    canvasnames = []
                    try:
                        if type(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]) is list:
                            canvascount = len(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"])
                            for canvasindex in range(canvascount):
                                hassource = False
                                if type(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["string"]) is list:
                                    stringcount = len(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["string"])
                                    for stringindex in range(stringcount):
                                        if img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["string"][stringindex]["@name"] == "source":
                                            rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["string"][stringindex]["@value"])
                                            hassource = True
                                else:
                                    if img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["string"]["@name"] == "source":
                                        rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["string"]["@value"])
                                        hassource = True
                                if hassource:
                                    canvasnames.append(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"][canvasindex]["@name"])
                        else:
                            hassource = False
                            if type(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["string"]) is list:
                                stringcount = len(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["string"])
                                for stringindex in range(stringcount):
                                    if img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["string"][stringindex]["@name"] == "source":
                                        rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["string"][stringindex]["@value"])
                                        hassource = True
                            else:
                                if img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["string"]["@name"] == "source":
                                    rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["string"]["@value"])
                                    hassource = True
                            if hassource:
                                canvasnames.append(img["imgdir"]["imgdir"][index]["imgdir"][numberedsub]["canvas"]["@name"])
                    except KeyError:
                        continue
                    if len(rawsources) <= 0 or len(canvasnames) <= 0:
                        continue
                    if len(rawsources) != len(canvasnames):
                        raise IndexError("Not exactly one source for each canvas. File: " + filepath)
                    if len(rawsources) == 1:
                        rawsources[0] = "../.." + rawsources[0][rawsources[0].find("img") + 3:]
                        img["imgdir"]["imgdir"][index]["imgdir"][numberedsub] = OrderedDict([("@name", numberedsubname), ("uol", OrderedDict([("@name", canvasnames[0]), ("@value", rawsources[0])]))])
                    else:
                        uollist = []
                        for rawsourceindex in range(len(rawsources)):
                            rawsources[rawsourceindex] = "../.." + rawsources[rawsourceindex][rawsources[rawsourceindex].find("img") + 3:]
                            uollist.append(OrderedDict([("@name", canvasnames[rawsourceindex]), ("@value", rawsources[rawsourceindex])]))
                        img["imgdir"]["imgdir"][index]["imgdir"][numberedsub] = OrderedDict([("@name", numberedsubname), ("uol", uollist)])
            else:
                numberedsubname = img["imgdir"]["imgdir"][index]["imgdir"]["@name"]
                rawsources = []
                canvasnames = []
                try:
                    if type(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]) is list:
                        canvascount = len(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"])
                        for canvasindex in range(canvascount):
                            hassource = False
                            if type(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["string"]) is list:
                                stringcount = len(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["string"])
                                for stringindex in range(stringcount):
                                    if img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["string"][stringindex]["@name"] == "source":
                                        rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["string"][stringindex]["@value"])
                                        hassource = True
                            else:
                                if img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["string"]["@name"] == "source":
                                    rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["string"]["@value"])
                                    hassource = True
                            if hassource:
                                canvasnames.append(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"][canvasindex]["@name"])
                    else:
                        hassource = False
                        if type(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["string"]) is list:
                            stringcount = len(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["string"])
                            for stringindex in range(stringcount):
                                if img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["string"][stringindex]["@name"] == "source":
                                    rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["string"][stringindex]["@value"])
                                    hassource = True
                        else:
                            if img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["string"]["@name"] == "source":
                                rawsources.append(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["string"]["@value"])
                                hassource = True
                        if hassource:
                            canvasnames.append(img["imgdir"]["imgdir"][index]["imgdir"]["canvas"]["@name"])
                except KeyError:
                    continue
                if len(rawsources) <= 0 or len(canvasnames) <= 0:
                    continue
                if len(rawsources) != len(canvasnames):
                    raise IndexError("Not exactly one source for each canvas. File: " + filepath)
                if len(rawsources) == 1:
                    rawsources[0] = "../.." + rawsources[0][rawsources[0].find("img") + 3:]
                    img["imgdir"]["imgdir"][index]["imgdir"] = OrderedDict([("@name", numberedsubname), ("uol", OrderedDict([("@name", canvasnames[0]), ("@value", rawsources[0])]))])
                else:
                    uollist = []
                    for rawsourceindex in range(len(rawsources)):
                        rawsources[rawsourceindex] = "../.." + rawsources[rawsourceindex][rawsources[rawsourceindex].find("img") + 3:]
                        uollist.append(OrderedDict([("@name", canvasnames[rawsourceindex]), ("@value", rawsources[rawsourceindex])]))
                    img["imgdir"]["imgdir"][index]["imgdir"] = OrderedDict([("@name", numberedsubname), ("uol", uollist)])

    filenamelen = len(filepath.split("/")[-1])
    newdir = filepath[:-1 * filenamelen] + "converted"
    os.makedirs(newdir, exist_ok=True)
    with open(newdir + "/" + filepath.split("/")[-1], mode="w", encoding="utf-8") as newimg:
        xmltodict.unparse(img, output=newimg, encoding="utf-8")
