# Takes hand-written recipes of the following format and writes new JavaScript dictionary
# syntax for them, for use with the Cody NPC:
#
# Fancy New Equip (equipId)
# 	*2 Craft Item (craftItemId)
# 	*77 Another Craft Item (anotherCraftItemId)
# 	*9 Yet Another Craft Item (yetAnotherCraftItemId)
#
# Another Fancy New Equip (anotherEquipId)
# 	*50 Yet Yet Another Craft Item...

lines = []
filename = input("Enter the filename, or relative/absolute path if not in this directory, of the *.txt file: ")
outfilename = input("Enter the filename, or relative/absolute path if not in this directory, of the desired output file: ")

with open(filename, "r") as f:
	lines = f.readlines()

recipes = {}
setitem = 0
recipe = []

for line in lines:
	if len(line) > 1:
		if line[0] != "	":
			setitem = int((line.split(" ")[-1]).strip("\n()"))
			continue
		else:
			line = line.rstrip().lstrip().strip("*)")
			split = line.split(" ")
			quantity = int(split[0].strip("("))
			itemid = int(split[-1].strip("("))
			recipe.append([itemid, quantity])
	else:
		recipes[str(setitem)] = recipe
		setitem = 0
		recipe = []

if setitem != 0:
	recipes[str(setitem)] = recipe

with open(outfilename, "w") as f:
	out = ""
	setitems = []
	for key in recipes.keys():
		setitems.append(key)
	for i in range(len(setitems)):
		out += "	" + setitems[i] + ": " + str(recipes[setitems[i]])
		if i < len(setitems) - 1:
			out += ",\n"
	f.write(out)
