# This was just a tool used to fix sloppy testing code in NPC scripts.
# NPC scripts should NOT explicitly call setStory() or setStoryPoints() on any characters,
# except for testing purposes. So this comments them out safely.
# Placed in scripts folder.

import os

for file in os.listdir("npc"):
    if file.endswith(".js"):
        hasstory = False
        linenumber = 0
        hascomment = False
        lines = []
        with open("npc/" + file, "r") as f:
            line = f.readline()
            while(line != ""):
                if "cm.getPlayer().setStory" in line:
                    hasstory = True
                    if "//" in line and line.find("//") < line.find("cm.getPlayer().setStory"):
                        hascomment = True
                        break
                    else:
                        hascomment = False
                        f.seek(0, 0)
                        lines = f.readlines()
                        break
                line = f.readline()
                linenumber += 1
        if hasstory and not hascomment:
            with open("npc/" + file, "w") as f:
                line = lines[linenumber]
                firstpart = line[0:line.find("cm.getPlayer().setStory")]
                secondpart = line[line.find("cm.getPlayer().setStory"):]
                lines[linenumber] = firstpart + "//" + secondpart
                f.writelines(lines)
