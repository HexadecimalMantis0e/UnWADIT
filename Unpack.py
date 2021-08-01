import os
import struct
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("wad")
    args = parser.parse_args()

    print("Unpacking WAD...")
    f0 = open(args.dir, "rb")
    f1 = open(args.wad, "rb")
    os.mkdir(args.wad[:-4])
    numOfFiles = struct.unpack('I', f0.read(4))[0]

    for i in range(0, numOfFiles):
        name = f0.read(0x40).decode()
        editedName = name.replace('\0', '')
        print(editedName)
        size = struct.unpack('I', f0.read(4))[0]
        address = struct.unpack('I', f0.read(4))[0]
        f1.seek(address, os.SEEK_SET)
        fileBytes = f1.read(size)
        filePath = os.path.join(args.wad[:-4], editedName)
        f2 = open(filePath, "wb")
        f2.write(fileBytes)
        f2.close()
    print("Done!")

    f0.close()
    f1.close()

if __name__ == "__main__":
    main()
