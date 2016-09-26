# Rewrites handwritten lists in collapsed format for easy transfer to Google Docs.

lines = []
filename = input("Enter the filename, or relative/absolute path if not in this directory, of the *.txt file: ")
stripbullets = input("Would you like to strip bullets (*, -, +, --, ++) from the list? (y/n): ")
stripb = False
if stripbullets == "y" or stripbullets == "Y":
	stripb = True

with open(filename, "r") as f:
	lines = f.readlines()

for i in range(len(lines)):
	lines[i] = lines[i].lstrip(" 	")
	if stripb:
		lines[i] = lines[i].lstrip("+-*")

with open(filename, "w") as f:
	for line in lines:
		if len(line) > 1:
			f.write(line)
