#!/bin/bash

# This uses gpg to encrypt every file in a directory as separate
# encrypted files

# Usage
# ./encrypt-all.sh ./dir-of-files-to-encrypt "PASSPHRASE"

PASSPHRASE="$1"

encrypted_file_name="Data/H3bitmap.lod.enc"
cat Data/H3bitmap.lod.enc.* > $encrypted_file_name

mkdir -p decrypted/Data

file_name="decrypted/${encrypted_file_name%.*}"

echo "Decrypting $encrypted_file_name"

gpg \
  --decrypt \
  --passphrase "$PASSPHRASE" \
  --batch \
  --output "$file_name" \
  --cipher-algo AES256 \
  "$encrypted_file_name"

echo "Output: $file_name"
