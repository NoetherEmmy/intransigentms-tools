# Used for modifying the string XML for skills, to change skill values (integers found in each level description)
# Supports adding/subtracting, multiplying, setting, but could easily be tweaked for a lot of things.
# Prints the number of individual values changed, for verification purposes.

filename = input("Enter the filename, or absolute/relative file path if not in this folder, of the String XML: ")
skillid = int(input("Enter the ID of the skill you wish to edit: "))
attribute = input("Enter the string after which the next number will be modified: ")
add = int(input("Enter how much you would like to add to the attribute at every level of the skill (can be negative): "))
multi = float(input("Enter how much you would like to multiply the attribute by at every level: "))
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
    skillstartindex = line.find("<imgdir name=\"" + str(skillid).zfill(7) + "\">")
    if skillstartindex == -1:
        raise ValueError("Could not find specified skill ID.")
    skillendindex = line.find("</imgdir>", skillstartindex)
    currentindex = line.find("<string name=\"h1\"", skillstartindex)
    currentindex = line.find(attribute, currentindex) + len(attribute)

    while currentindex > skillstartindex and currentindex < skillendindex:
        thevalue = ""
        valuefirstindex = -1
        while True:
            if line[currentindex] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ','] and currentindex < skillendindex:
                thevalue += line[currentindex]
                valuefirstindex = currentindex
                currentindex += 1
                break
        while line[currentindex] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ',']:
            thevalue += line[currentindex]
            currentindex += 1

        thevalue = thevalue.replace(",", "")

        newvalue = 0
        if setto != -60001:
            newvalue = setto
        else:
            newvalue = int(int(thevalue) * multi)
            newvalue += add
        newvalue = str(newvalue)
        
        beginning = line[:valuefirstindex]
        end = line[currentindex:]
        line = beginning + newvalue + end
        attributeschangedcount += 1

        if len(newvalue) != len(thevalue):
            difference = len(newvalue) - len(thevalue)
            skillendindex += difference
            currentindex += difference

        currentindex = line.find(attribute, currentindex) + len(attribute)
    
    out = line

with open(filename, "w") as f:
    f.write(out)

print(attributeschangedcount)
