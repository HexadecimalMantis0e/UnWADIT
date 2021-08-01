import os
import struct
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()

    address = 0x00
    needPadCheck = False

    print("Packing WAD...")
    fileList = os.listdir(args.directory)
    f0 = open(args.directory + ".DIR", "wb")
    f1 = open(args.directory + ".WAD", "wb")
    numOfFiles = len(fileList)
    f0.write(struct.pack('I', numOfFiles))

    for fileName in fileList:
        f0.write(fileName.encode())
        padLength = 0x40 - len(fileName)
        f0.write(bytearray([0x00]) * padLength)
        filePath = os.path.join(args.directory, fileName)
        f2 = open(filePath, "rb")
        header = f2.read(4)

        # pad everything that isn't a strat WAD
        if header != "BIGB".encode():
            needPadCheck = True
        else:
            print(fileName)

        f2.seek(0x00, os.SEEK_END)
        size = f2.tell()
        f2.seek(0x00, os.SEEK_SET)

        f0.write(struct.pack('I', size))
        f0.write(struct.pack('I', address))

        if needPadCheck == True:
            print("Padding " + fileName)
            paddingSize = 0x800 - (size % 0x800)
            address += paddingSize

        fileBytes = f2.read(size)
        f1.write(fileBytes)
        address += size

        if needPadCheck == True:
            f1.write(bytearray([0x00]) * paddingSize)
            needPadCheck = False
        f2.close()
    print("Done!")

    f0.close()
    f1.close()

if __name__ == "__main__":
    main()
