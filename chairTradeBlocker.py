# Used to trade block all chairs (cannot be traded or dropped).
# To use this, export the 0301.img from your Item.wz file using HaRepacker.
# More specifically, export as classic XML.

from collections import OrderedDict
import os
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
filepath = filedialog.askopenfilename(filetypes=[("XML files", ".xml")], title="Select the dumped 0301.img.xml file you'd like to trade block:")

fp = open(filepath)
img = xmltodict.parse(fp.read())
fp.close()

for chair in img["imgdir"]["imgdir"]:
    for chairpart in chair["imgdir"]:
        if chairpart["@name"] == "info":
            infohastradeblock = False
            for infoint in chairpart["int"]:
                if infoint["@name"] == "tradeBlock":
                    infohastradeblock = True
                    break
            if not infohastradeblock:
                chairpart["int"].insert(len(chairpart["int"]) - 2, OrderedDict([("@name", "tradeBlock"), ("@value", "1")]))

filenamelen = len(filepath.split("/")[-1])
newdir = filepath[:-1 * filenamelen] + "converted"
os.makedirs(newdir, exist_ok=True)
with open(newdir + "/" + filepath.split("/")[-1], mode="w", encoding="utf-8") as newimg:
    xmltodict.unparse(img, output=newimg, encoding="utf-8")
