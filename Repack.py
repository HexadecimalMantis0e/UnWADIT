import os
import struct
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("directory")
args = parser.parse_args()

address = 0x00
needPadCheck = False

print "Packing WAD..."

list = os.listdir(args.directory)
f0 = open(args.directory+".WAD","wb")
f1 = open(args.directory+".DIR","wb")
number_files = len(list)
f1.write(struct.pack("i", number_files))

for filename in os.listdir(args.directory):
    f1.write(filename)
    padLength = 0x40 - len(filename)
    f1.write(bytearray([0])*padLength)
    fpath = os.path.join(args.directory, filename)
    f2 = open(fpath, "rb")

    header = f2.read(4)

    # pad everything that isn't a strat
    if header != "BIGB":
        needPadCheck = True

    f2.seek(0x00, os.SEEK_END)
    size = f2.tell()
    f2.seek(0x00, os.SEEK_SET)

    f1.write(struct.pack("i", size))
    f1.write(struct.pack("i", address))

    if needPadCheck == True:
        print "padding " + filename
        paddingSize = 0x800 - (size % 0x800)
        address += paddingSize

    filebytes = f2.read(size)
    f0.write(filebytes)
    address += size
    if needPadCheck == True:
        f0.write(bytearray([0])*paddingSize)
        needPadCheck = False
    f2.close()

f0.close()
f1.close()
