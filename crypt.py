#!/usr/bin/env python3

import argparse
import os
import shutil
from pathlib import Path
from pprint import pprint

parser = argparse.ArgumentParser(description="Encrypts and decrypts Heroes 3 data")
parser.add_argument("-p", "--password", required=True)
parser.add_argument("-e", "--encrypt", action="store_true")
parser.add_argument("-d", "--decrypt", action="store_true")
args = vars(parser.parse_args())

original = Path(r"HoMM3_data")
encrypted = original.parent / f"{original.stem}_encrypted"
decrypted = original.parent / f"{original.stem}_decrypted"

if args["encrypt"]:
    src = original
    dest = encrypted
elif args["decrypt"]:
    src = encrypted
    dest = decrypted
else:
    print("Specify -e to encrypt or -d to decrypt")
    exit(1)

shutil.rmtree(dest, ignore_errors=True)
shutil.copytree(src, dest, dirs_exist_ok=True)

if args["decrypt"]:
    part_0 = dest / "Data/H3bitmap.lod.enc.00"
    part_1 = dest / "Data/H3bitmap.lod.enc.01"
    combined = dest / "Data/H3bitmap.lod.enc"
    with open(combined, "wb") as combined_f, open(part_0, "rb") as part_0_f, open(part_1, "rb") as part_1_f:
        combined_f.write(part_0_f.read())
        combined_f.write(part_1_f.read())
    os.remove(part_0)
    os.remove(part_1)

for f in dest.glob("**/*"):
    if f.is_file():
        # command based on https://gist.github.com/johnnyopao/33c6500bda474a7afb33207489d8e8e5
        if args["encrypt"]:
            print(f"Encrypting {f}")
            command = f'gpg --passphrase "{args["password"]}" --batch --output "{f}.enc" --symmetric --cipher-algo AES256 "{f}"'
        else:
            print(f"Decrypting {f}")
            command = f'gpg --decrypt --passphrase "{args["password"]}" --batch --output "{f.parent/f.stem}" --cipher-algo AES256 "{f}"'
        # print(command)
        os.system(command)
        os.remove(f)

if args["encrypt"]:
    # split file since GitHub only allows files up to 100 MB
    # https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
    command = f"split --bytes 100M --numeric-suffixes --suffix-length=2 {dest/'Data/H3bitmap.lod.enc'} {dest/'Data/H3bitmap.lod.enc.'}"
    print(command)
    os.system(command)
    os.remove(dest/"Data/H3bitmap.lod.enc")
