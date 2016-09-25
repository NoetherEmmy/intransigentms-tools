# Searches for all mobs that have deadly attacks (known as 1/1 attacks/mechanic).
# These lower players' HP and MP to 1 automatically.
# Must be placed in <server>/wz directory.

import os

candidates = []

for file in os.listdir("Mob.wz"):
    if file.endswith(".xml"):
        with open("Mob.wz/" + file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "<int name=\"deadlyAttack\" value=\"1\"" in line:
                    candidates.append(file)
                    break

stripped = []

for c in candidates:
    stripped.append(c.strip(".img.xml"))

string = "("

for s in range(len(stripped)):
    string += stripped[s]
    if s < len(stripped) - 1:
        string += ", "
    else:
        string += ")"

print(string)
