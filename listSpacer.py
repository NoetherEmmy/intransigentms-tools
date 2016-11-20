# Takes in comma-spaced multi-line arrays and makes
# the items spaced evenly.

import re

filename = input("Filename: ")
lines = []

with open(filename, "r") as f:
    lines = f.readlines()

splitted = [[s.strip() for s in line.split(",")]
            for line in lines if "," in line]

longestline = 0
for linearray in splitted:
    if len(linearray) > longestline:
        longestline = len(linearray)

spaces = [max(lenarray)
          for lenarray in [[len(line[a])
                            for line in splitted if len(line) > a]
                           for a in range(longestline)]]

out = ""
for line in lines:
    if "," in line:
        leadingwhite = re.match(r"\s*", line).group()
        i = 0
        stripsplit = [w.strip() for w in line.split(",")][:-1]
        for word in stripsplit:
            leadingwhite += word + ","
            if i < len(stripsplit) - 1:
                leadingwhite += "".join(
                    [" " for _ in range(spaces[i] - len(word) + 1)]
                )
            i += 1
        out += leadingwhite + "\n"
    else:
        out += line

newfilename = ".".join(filename.split(".")[:-1]) + \
    ".spaced." + filename.split(".")[-1]
with open(newfilename, "w") as f:
    f.write(out)
