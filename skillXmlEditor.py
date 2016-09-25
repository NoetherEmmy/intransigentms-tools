# Used for modifying skill XMLs (from Skill.wz) to change skill values (in the "level" nodes)
# Supports adding/subtracting, multiplying, setting, but could easily be tweaked for a lot of things.
# Prints the number of individual values changed, for verification purposes.

filename = input("Enter the filename, or absolute/relative file path if not in this folder, of the skill XML: ")
skillid = int(input("Enter the ID of the skill you wish to edit: "))
attribute = input("Enter the attribute you wish to modify (e.g. \"mad\" for magic attack damage): ")
add = int(input("Enter how much you would like to add to the attribute at every level of the skill (can be negative): "))
multi = float(input("Enter how much you would like to multiply the atrribute by at every level: "))
setto = 0
try:
    setto = int(input("Enter what you would like to set the attribute to at all levels (enter anything that is not an integer to ignore): "))
except:
    setto = -60001 # Magic number that I assume no one will enter

out = ""
attributeschangedcount = 0

with open(filename, "r") as f:
    lines = f.readlines()
    if len(lines) > 1:
        raise IOError("XML file is not all in one line.")
    line = lines[0]
    skillstartindex = line.find("<imgdir name=\"" + str(skillid) + "\">")
    if skillstartindex == -1:
        raise ValueError("Could not find specified skill ID.")
    skillstartindex = line.find("<imgdir name=\"level\">", skillstartindex + 5)
    skillendindex = line.find("<imgdir name=\"effect\">", skillstartindex + 5)
    if skillendindex == -1:
        skillendindex = len(line)
    attributeindex = line.find("name=\"" + attribute + "\"", skillstartindex + 5)
    while attributeindex != -1 and attributeindex < skillendindex:
        valuestart = line.find("value=\"", attributeindex)
        beginning = line[:valuestart + 7]
        valueend = line.find("\"/", valuestart + 7)
        value = line[valuestart + 7:valueend]
        end = line[valueend:]
        newvalue = 0
        if setto != -60001:
            newvalue = setto
        else:
            newvalue = int(value) * multi
            newvalue += add
        newvalue = str(newvalue)
        if len(newvalue) != len(value):
            difference = len(newvalue) - len(value)
            skillendindex += difference
        value = newvalue
        line = beginning + value + end
        attributeschangedcount += 1
        attributeindex = line.find("name=\"" + attribute + "\"", attributeindex + 2)
    out = line

with open(filename, "w") as f:
    f.write(out)

print(attributeschangedcount)
