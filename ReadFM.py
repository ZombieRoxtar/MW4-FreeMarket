#
# This script digests a black market file for readability.
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
    file_size = os.path.getsize(name)
    byte = f.read(28) # Skip header
    week = 0
    print("Week 0")
    while byte != b"":
        # Loop here because not every week is used
        for i in range(week, value(f.read(4))):
            week += 1
            print("Week", week)
        members = value(f.read(4)) # How many new weapons?
        for i in range(0, members):
            len = value(f.read(4))
            print(f.read(len).decode())
            f.read(1) # Skip null termination
        members = value(f.read(4)) # How many new mechs?
        for i in range(0, members):
            len = value(f.read(4))
            print(f.read(len).decode())
            f.read(1) # Skip null termination
        byte = f.read(24) # End of Week

        # Break out at the end of the file
        read_size = f.tell()
        if read_size == file_size:
            break
