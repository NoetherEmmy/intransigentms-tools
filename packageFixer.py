# This script is for ensuring the compatibility of JS scripts with Java versions 1.8+
# Once this tool is run on the scripts folder, no futher changes should be required; Nashorn
# (the new Java 1.8+ script engine) should be able to parse the scripts just fine.
# This must be placed in the main folder.

import os

def linePrepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

for dirpath, dirnames, filenames in os.walk("./scripts"):
	for file in filenames:
		if file[len(file) - 3:] == ".js":
			linePrepender(os.path.join(dirpath, file), "load('nashorn:mozilla_compat.js');")

			lines = []
			with open(os.path.join(dirpath, file), "r") as f:
				lines = f.readlines()
			for i in range(len(lines)):
				if "net.sf." in lines[i] and "Packages" not in lines[i]:
					lines[i] = lines[i].replace("net.sf.", "Packages.net.sf.")
			with open(os.path.join(dirpath, file), "w") as f:
				f.writelines(lines)