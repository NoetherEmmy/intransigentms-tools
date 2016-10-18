# Prints a list of the IDs of all equipments that have
# no associated string (name and/or description).
# Can be tweaked to find missing strings for other things
# as well.
# Must be placed in /wz folder.

from os import walk
import mmap

missing = []

for dirpath, dirnames, filenames in walk("./Character.wz"):
	for file in filenames:
		_id = 0
		try:
			_id = int(file[:8])
		except ValueError:
			continue
		if _id >= 1000000:
			with open("./String.wz/Eqp.img.xml", "rb", 0) as stringdata:
				with mmap.mmap(stringdata.fileno(), 0, access=mmap.ACCESS_READ) as stringmemory:
					stringbytes = ('<imgdir name="' + str(_id) + '">').encode('UTF-8')
					if stringmemory.find(stringbytes) == -1:
						missing.append(_id)

print(missing)
