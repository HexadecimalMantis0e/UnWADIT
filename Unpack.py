import os
import struct
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("dir")
parser.add_argument("wad")
args = parser.parse_args()

print "Unpacking WAD..."

f0 = open(args.dir,"rb")
f1 = open(args.wad,"rb")
os.mkdir(str(args.wad[:-3]))

amount = struct.unpack('i', f0.read(4))[0]

for i in range(0,amount):
    name = f0.read(0x40)
    newname = name.replace('\0', '')
    print newname
    size = struct.unpack('i', f0.read(4))[0]
    address = struct.unpack('i', f0.read(4))[0]
    f1.seek(address, os.SEEK_SET)
    filebytes = f1.read(size)
    fpath = os.path.join(args.wad[:-3], newname)
    f2 = open(fpath, "wb")
    f2.write(filebytes)
    f2.close()

print "Done!"

f0.close()
f1.close()
