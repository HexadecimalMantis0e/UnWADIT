import os
import struct
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("directory")
args = parser.parse_args()

address = 0x00
needPadCheck = False

print("Packing WAD...")
fileList = os.listdir(args.directory)
f0 = open(args.directory+".WAD", "wb")
f1 = open(args.directory+".DIR", "wb")
numOfFiles = len(fileList)
f1.write(struct.pack('I', numOfFiles))

for fileName in fileList:
    f1.write(fileName.encode())
    padLength = 0x40 - len(fileName)
    f1.write(bytearray([0x00]) * padLength)
    filePath = os.path.join(args.directory, fileName)
    f2 = open(filePath, "rb")
    header = struct.unpack('I', f2.read(4))[0]

    # pad everything that isn't a strat WAD
    if header != 0x42474942:
        needPadCheck = True
    else:
        print(fileName)

    f2.seek(0x00, os.SEEK_END)
    size = f2.tell()
    f2.seek(0x00, os.SEEK_SET)

    f1.write(struct.pack('I', size))
    f1.write(struct.pack('I', address))

    if needPadCheck == True:
        print("Padding " + fileName)
        paddingSize = 0x800 - (size % 0x800)
        address += paddingSize

    fileBytes = f2.read(size)
    f0.write(fileBytes)
    address += size
    if needPadCheck == True:
        f0.write(bytearray([0x00]) * paddingSize)
        needPadCheck = False
    f2.close()
print("Done!")

f0.close()
f1.close()
