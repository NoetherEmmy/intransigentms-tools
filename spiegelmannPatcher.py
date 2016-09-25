# Simply updates all Spiegelmann NPCs to have same script as the first one (ID 2042000).
# Must be placed in NPC script folder.

import os
import shutil

ids = [2042001, 2042002, 2042005, 2042006, 2042007]

for id in ids:
	os.remove(str(id) + '.js')
	shutil.copy('2042000.js', str(id) + '.js')
