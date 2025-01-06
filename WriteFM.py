#
# This script writes an extremely short black market file.
# Usage: python WriteFM.py 8935_wodrgcampaign.blackmarket
#

import sys
import os

if len(sys.argv) <= 1:
    print("No file specified!")
    exit()

name = sys.argv[1]

with open(name, 'wb') as w:
    # The fist eight bytes are the length of the header including itself
    w.write(b'\x1C\x00\x00\x00')
    w.write(b'\x00\x00\x00\x00')
    w.write(b'\xFF\xFF\xFF\x7F') # This is also the week seperator
    w.write(b'\xFF\xFF\xFF\x7F')
    w.write(b'\xFF\xFF\xFF\x7F')
    w.write(b'\xFF\xFF\xFF\x7F')
    w.write(b'\xFF\xFF\xFF\x7F')
    w.write(b'\x00\x00\x00\x00') # Starting Week number
    w.write(b'\x01\x00\x00\x00') # Weapon Count
    w.write(b'\x05\x00\x00\x00') # Name Length
    w.write("ssrm2\0".encode())  # Name, Null Terminated
    w.write(b'\x01\x00\x00\x00') # Mech Count
    w.write(b'\x05\x00\x00\x00') # Name Length
    w.write("atlas\0".encode())  # Name, Null Terminated
    w.write(b'\x00\x00\x00\x00') # Footer for the end of the last week
