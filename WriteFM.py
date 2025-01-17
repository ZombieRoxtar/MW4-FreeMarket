#
# This script writes a new black market file from JSON.
# Usage: python WriteFM.py 8935_wodrgcampaign.blackmarket
#

import sys

if len(sys.argv) <= 1:
    print("No file specified!")
    exit()
name = sys.argv[1]

prevWeek = -1
def NewWeek(num, count):
    global prevWeek
    if num > prevWeek:
        if prevWeek == -1: # Start File
            w.write(b'\x1C\x00\x00\x00') # Length of the week separator
        w.write(b'\x00\x00\x00\x00')
        w.write(b'\xFF\xFF\xFF\x7F')
        w.write(b'\xFF\xFF\xFF\x7F')
        w.write(b'\xFF\xFF\xFF\x7F')
        w.write(b'\xFF\xFF\xFF\x7F')
        w.write(b'\xFF\xFF\xFF\x7F')
        # Add week number. Seems to be a signed int... Makes you wonder.
        w.write((num).to_bytes(4, byteorder = 'little', signed = True))
        prevWeek = num
    if prevWeek == num: # New Weapon or Mech list
        w.write((count).to_bytes(4, byteorder = 'little', signed = True))

def AddItem(name):
    w.write((len(name)).to_bytes(4, byteorder = 'little', signed = True)) # Name Length
    w.write(bytes(name + "\0", "ascii")) # Name, Null Terminated

with open(name, 'wb') as w:
    r = open(name + ".json", "r")
    week = -1
    eList = []
    line = r.readline()
    while line != "":
        if line == "    \"Week\":\n":
            # Keep counting weeks because they can be skipped
            week += 1
        itemLine = True
        # If we hit a JSON header...
        if line == "\"Market\"\n" or \
           line == "{\n" or \
           line == "    \"Week\":\n" or \
           line == "    {\n" or \
           line == "        \"Weapons\":\n" or \
           line == "        \"Mechs\":\n" or \
           line == "        {\n" or \
           line == "        },\n" or \
           line == "    },\n" or \
           line == "    }\n" or \
           line == "}\n":
            itemLine = False
            # ...dump my mech/weapons list...
            if len(eList):
                NewWeek(week, len(eList))
                for item in eList:
                    AddItem(item)
            # ...then clear it.
            eList = []
        if itemLine == True:
            # Append another item
            eList.append(line.lower().strip().replace("\"", ""))
        line = r.readline()
    w.write(b'\x00\x00\x00\x00') # Footer for the end of the last week
