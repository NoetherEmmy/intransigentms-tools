#!/usr/bin/env python

"""
Python 2.7.x

This script takes in an .html/.htm file of a
`bbb.hidden-street.net`_ webpage containing monster info.
It extracts the monster(s)' drop information and uses it
to generate a drop table in the form of an ``INSERT INTO``
statement in an .sql file.

That means that this script has to be run where it has top
level access to server XML files, viz. <server_root>/wz
or just anywhere that .wz files are extracted using
HaRepacker to "Private Server XML."
"""

from __future__ import division, print_function
from codecs import open as o
import re

tablere = re.compile(r'<table id="[0-9]+" class="monster">')
endtablere = re.compile(r'</table>')
mobnamere = re.compile(r'(?<=<strong>)[^<>]+(?=</strong>)')
itemre = re.compile(r'(<a href="[^" ]+" alt="[^" ]+">)([^<>]+)(?=</a>)')
genderre = re.compile(r'(?i)(?<=[(\[])([FM]|(Female)|(Male))(?=[)\]])')
scrollsuccessre = re.compile(r'[1-9][0-9][0-9]?%')
idrestart = r'(?i)([0-9]+)(">)(<string name="desc" value="[^"]+"/>)?' + \
            r'(?=<string name="name" value=" *'
idreend = r' *"/>)'
scrollidreend = r' ?[0-9]*%?"/>)'
etcstring = '<strong>Etc. drop:</strong>'
equipstring = '<strong>Common equipment:</strong>'
orestring = '<strong>Ore drop:</strong>'
makerstring = '<strong>Maker item:</strong>'
usestring = '<strong>Useable drop:</strong>'
endusestring = '</tr>'
xmlentities = {
    '&': "&amp;",
    "'": "&apos;",
    '>': "&gt;",
    '<': "&lt;",
    '"': "&quot;",
}


def xmlescape(string):
    for char, entity in xmlentities.iteritems():
        string = string.replace(char, entity)
    return string


filename = raw_input("Enter the name of the HTML file to be scanned: ")
tablestrings = []
entries = []

print("")
with o(filename, "r", "utf-8") as f:
    tablestrings = tablere.split(f.read())[1:]

rsplit = tablestrings[len(tablestrings) - 1]
tablestrings[len(tablestrings) - 1] = endtablere.split(rsplit)[0]

tableindex = -1
for tablestring in tablestrings:
    tableindex += 1
    index = 0
    mobid = 0

    """ Mob """
    mobnamematch = mobnamere.search(tablestring, index)
    mobname = ""
    if mobnamematch:
        mobname = mobnamematch.group().strip()
        index = mobnamematch.end()
    else:
        print("Could not find initial mob name in " +
              filename + " in table " + str(tableindex))

    with o("String.wz/Mob.img.xml", "r", "utf-8") as mobstringf:
        pattern = idrestart + re.escape(xmlescape(mobname)) + idreend
        mobidmatch = re.search(pattern, mobstringf.read())
        if mobidmatch:
            mobid = int(mobidmatch.group(1))
        else:
            print("Could not find mob ID for mob with name " + mobname)

    """ Etc """
    index = tablestring.find(etcstring, index)
    equipstart = tablestring.find(equipstring, index)
    etcmatches = itemre.finditer(tablestring, index, equipstart)
    with o("String.wz/Etc.img.xml", "r", "utf-8") as etcstringf:
        etcstringfcontents = etcstringf.read()
        for etcmatch in etcmatches:
            etcname = etcmatch.group(2)
            pattern = idrestart + re.escape(xmlescape(etcname)) + idreend
            etcidmatch = re.search(pattern, etcstringfcontents)
            if etcidmatch:
                entries.append((mobid, int(etcidmatch.group(1)), 5, etcname))
            else:
                print("Could not find item ID for etc with name " + etcname)

    """ Equip """
    index = equipstart
    orestart = tablestring.find(orestring, index)
    eqpmatches = itemre.finditer(tablestring, index, orestart)
    with o("String.wz/Eqp.img.xml", "r", "utf-8") as eqpstringf:
        eqpstringfcontents = eqpstringf.read()
        for eqpmatch in eqpmatches:
            eqpname = eqpmatch.group(2)
            gendermatch = genderre.search(eqpname)
            if gendermatch:
                gender = gendermatch.group()[0].upper()
                eqpname = eqpname[:gendermatch.start() - 1].strip()
                pattern = idrestart + re.escape(xmlescape(eqpname)) + idreend
                eqpidmatches = list(re.finditer(pattern, eqpstringfcontents))

                if len(eqpidmatches) < 1:
                    print("Could not find item ID for equip with name " +
                          eqpname)

                eqpidmatchindex = -1
                for eqpidmatch in eqpidmatches:
                    eqpidmatchindex += 1
                    if eqpidmatchindex == 0 and \
                       len(eqpidmatches) > 1 and gender == "F":
                        continue
                    entries.append(
                        (mobid, int(eqpidmatch.group(1)), 650, eqpname))
                    break

                continue

            pattern = idrestart + re.escape(xmlescape(eqpname)) + idreend
            eqpidmatch = re.search(pattern, eqpstringfcontents)
            if eqpidmatch:
                entries.append((mobid, int(eqpidmatch.group(1)), 650, eqpname))
            else:
                print("Could not find item ID for equip with name " + eqpname)

    """ Ore """
    index = orestart
    makerstart = tablestring.find(makerstring, index)
    orematches = itemre.finditer(tablestring, index, makerstart)
    with o("String.wz/Etc.img.xml", "r", "utf-8") as orestringf:
        orestringfcontents = orestringf.read()
        for orematch in orematches:
            orename = orematch.group(2)
            pattern = idrestart + re.escape(xmlescape(orename)) + idreend
            oreidmatch = re.search(pattern, orestringfcontents)
            if oreidmatch:
                entries.append((mobid, int(oreidmatch.group(1)), 240, orename))
            else:
                print("Could not find item ID for ore with name " + orename)

    """ Maker """
    # Skip this, at least for now
    index = makerstart
    usestart = tablestring.find(usestring, index)

    """ Use """
    index = usestart
    useend = tablestring.find(endusestring, index)
    usematches = itemre.finditer(tablestring, index, useend)
    with o("String.wz/Consume.img.xml", "r", "utf-8") as usestringf:
        usestringfcontents = usestringf.read()
        for usematch in usematches:
            usename = usematch.group(2)
            if usename == "The Magic Rock":
                entries.append((mobid, 4006000, 600, "The Magic Rock"))
                continue
            if usename == "The Summoning Rock":
                entries.append((mobid, 4006001, 600, "The Summoning Rock"))
                continue
            if scrollsuccessre.search(usename, len(usename) - 4):
                isscroll = usename[-1] != ')'
                chance = 850
                if not isscroll:
                    chance = 10000
                rate = int(usename[-4:].strip(" %()"))
                usename = usename[:-4].strip(" ()")
                if "Overall Armor" in usename:
                    usename = usename.replace(
                        "Overall Armor", r'Overall ?(Armor)?')
                    pattern = idrestart + xmlescape(usename) + scrollidreend
                elif "Overall" in usename:
                    usename = usename.replace("Overall", r'Overall ?(Armor)?')
                    pattern = idrestart + xmlescape(usename) + scrollidreend
                else:
                    pattern = idrestart + \
                        re.escape(xmlescape(usename)) + scrollidreend
                useidmatches = list(re.finditer(pattern, usestringfcontents))

                if len(useidmatches) < 1:
                    print(
                        "Could not find item ID for use with name " + usename)

                useidmatchindex = -1
                for useidmatch in useidmatches:
                    useidmatchindex += 1
                    if isscroll:
                        if useidmatchindex == 0 and \
                           len(useidmatches) == 2 and rate != 100 and \
                           rate != 70:
                            continue
                        if useidmatchindex == 0 and \
                           len(useidmatches) >= 3 and rate != 100:
                            continue
                        if useidmatchindex == 1 and \
                           len(useidmatches) == 3 and rate != 60:
                            continue
                        if useidmatchindex == 1 and \
                           len(useidmatches) > 3 and rate != 70:
                            continue
                        if useidmatchindex == 2 and \
                           len(useidmatches) > 4 and rate != 60:
                            continue
                        if useidmatchindex == 3 and \
                           len(useidmatches) > 4 and rate != 30:
                            continue
                    else:
                        if useidmatchindex == 0 and \
                           len(useidmatches) == 2 and rate != 70:
                            continue
                        if useidmatchindex == 0 and \
                           len(useidmatches) == 3:
                            continue
                        if useidmatchindex == 1 and \
                           len(useidmatches) == 3 and rate != 70:
                            continue
                    entries.append(
                        (mobid, int(useidmatch.group(1)), chance, usename))
                    break

                continue

            pattern = idrestart + re.escape(xmlescape(usename)) + idreend
            useidmatch = re.search(pattern, usestringfcontents)
            if useidmatch:
                chance = 350
                useid = int(useidmatch.group(1))
                if useid // 10000 > 203:
                    chance = 850
                entries.append((mobid, useid, chance, usename))
            else:
                print("Could not find item ID for use with name " + usename)

entries = sorted(entries, key=lambda e: (e[0], e[2], e[1]))
out = "INSERT INTO monsterdrops\n" + \
      "(monsterid, itemid, chance)\n" + \
      "VALUES\n"
for entry in entries:
    monsterid, itemid, chance, itemname = entry
    out += "("
    out += str(monsterid)
    out += ", "
    out += str(itemid)
    out += ", "
    out += str(chance)
    out += "), -- "
    out += itemname
    out += "\n"

i = out.rfind(",")
out = out[:i] + ";" + out[i + 1:]
with o(filename + ".sql", "w", "utf-8") as f:
    f.write(out)
