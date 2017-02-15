#!/usr/bin/env python

"""
Python 2.7.x

This script is just a modification of dropTableGenerator.py
that should be run *before* that script is used.

Running this script, again, in the /wz/ directory, with access
to /wz/String.wz/ as the string data from the version that
**is being imported**, and /wz/String2.wz/ as the string
data from the version that you already have, this script
will emit all of the discrepancies between the items listed
to be dropped in the .html/.htm file and the items you already
have.

I.e., this script can tell you which items need to be ported
to your version in order to create a drop table that conforms
to what is in the .html/.htm file.
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
mismatches = {}

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
    etcmatches = list(itemre.finditer(tablestring, index, equipstart))
    with o("String.wz/Etc.img.xml", "r", "utf-8") as etcstringf:
        etcstringfcontents = etcstringf.read()
        for etcmatch in etcmatches:
            etcname = etcmatch.group(2).strip()
            pattern = idrestart + re.escape(xmlescape(etcname)) + idreend
            etcidmatch = re.search(pattern, etcstringfcontents)
            if etcidmatch:
                etcid = int(etcidmatch.group(1))
                entries.append((mobid, etcid, 5, etcname))
                with o("String2.wz/Etc.img.xml", "r", "utf-8") as etcstringf2:
                    etcstringf2contents = etcstringf2.read()
                    pattern = idrestart + \
                        re.escape(xmlescape(etcname)) + idreend
                    etcidmatch = re.search(pattern, etcstringf2contents)
                    if not etcidmatch:
                        mismatches[etcid] = etcname
            else:
                print("Could not find item ID for etc with name " + etcname)

    """ Equip """
    index = equipstart
    orestart = tablestring.find(orestring, index)
    eqpmatches = list(itemre.finditer(tablestring, index, orestart))
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
                eqpid = int(eqpidmatch.group(1))
                entries.append((mobid, eqpid, 650, eqpname))
                with o("String2.wz/Eqp.img.xml", "r", "utf-8") as eqpstringf2:
                    eqpstringf2contents = eqpstringf2.read()
                    eqpidmatch = re.search(pattern, eqpstringf2contents)
                    if not eqpidmatch:
                        mismatches[eqpid] = eqpname
            else:
                print("Could not find item ID for equip with name " + eqpname)

    """ Ore """
    index = orestart
    makerstart = tablestring.find(makerstring, index)
    orematches = list(itemre.finditer(tablestring, index, makerstart))
    with o("String.wz/Etc.img.xml", "r", "utf-8") as orestringf:
        orestringfcontents = orestringf.read()
        for orematch in orematches:
            orename = orematch.group(2)
            pattern = idrestart + re.escape(xmlescape(orename)) + idreend
            oreidmatch = re.search(pattern, orestringfcontents)
            if oreidmatch:
                oreid = int(oreidmatch.group(1))
                entries.append((mobid, oreid, 240, orename))
                with o("String2.wz/Etc.img.xml", "r", "utf-8") as orestringf2:
                    orestringf2contents = orestringf2.read()
                    oreidmatch = re.search(pattern, orestringf2contents)
                    if not oreidmatch:
                        mismatches[oreid] = orename
            else:
                print("Could not find item ID for ore with name " + orename)

    """ Maker """
    # Skip this, at least for now
    index = makerstart
    usestart = tablestring.find(usestring, index)

    """ Use """
    index = usestart
    useend = tablestring.find(endusestring, index)
    usematches = list(itemre.finditer(tablestring, index, useend))
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
                with o("String2.wz/Consume.img.xml", "r", "utf-8") as \
                        usestringf2:
                    usestringf2contents = usestringf2.read()
                    useidmatch = re.search(pattern, usestringf2contents)
                    if not useidmatch:
                        mismatches[useid] = usename
            else:
                print("Could not find item ID for use with name " + usename)

print("~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
for itemid, name in mismatches.items():
    print(itemid, name)
