#!/bin/bash

# This uses gpg to encrypt every file in a directory as separate
# encrypted files

# Usage
# ./encrypt-all.sh ./dir-of-files-to-encrypt "PASSPHRASE"

PASSPHRASE="$1"

file_name="Data/H3bitmap.lod"
enc_name="$file_name.enc"

echo "Encrypting $file_name"

gpg \
  --passphrase "$PASSPHRASE" \
  --batch \
  --output "$file_name.enc" \
  --symmetric \
  --cipher-algo AES256 \
  "$file_name"
