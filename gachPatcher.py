#!/usr/bin/env python

"""
Any version of Python

Very simply makes all gachapon NPCs have an identical
script to the first one (ID 9100100).

Must be placed in NPC script folder.
"""

import os
import shutil

for id_ in range(9100101, 9100112):
    os.remove(str(id_) + ".js")
    shutil.copy("9100100.js", str(id_) + ".js")
