# Encrypted Heroes 3 data

This data is needed to run VCMI's unit tests

Created by copying the folders `Data`, `Maps` from a Heroes 3 installation into the folder `HoMM3_data`, deleting `Data/VIDEO.VID` and executing this command: 

`./crypt.py -p "password" -e`

The data can be decrypted like this:

`./crypt.py -p "password" -d`