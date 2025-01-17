#
# This script converts a black market file to JSON for easy editing.
# Usage: python ReadFM.py 8935_wodrgcampaign.blackmarket
#

import sys
import os

def value(b):
    return int.from_bytes(b, "little")

if len(sys.argv) <= 1:
    print("No file specified!")
    exit()
name = sys.argv[1]

with open(name, "rb") as f:
    w = open(name + ".json", "w")
    file_size = os.path.getsize(name)
    byte = f.read(28) # Skip header
    w.write("\"Market\"\n{\n")
    week = 0
    w.write("    \"Week\":\n    {\n")
    while byte != b"":
        # Not every week is used
        for _w in range(week, value(f.read(4))):
            week += 1
            w.write("    },\n    \"Week\":\n    {\n")
        for m in range(0, 2):
            members = value(f.read(4)) # How many new items?
            t = "Weapons"
            if m == 1:
                t = "Mechs"
            w.write("        \"" + t + "\":\n        {\n")
            for _i in range(0, members):
                len = value(f.read(4))
                w.write("            \"")
                w.write(f.read(len).decode())
                w.write("\"\n")
                f.read(1) # Skip null termination
            w.write("        },\n")
        byte = f.read(24) # End of Week

        # Break out at the end of the file
        read_size = f.tell()
        if read_size == file_size:
            w.write("    }\n}\n")
            break
