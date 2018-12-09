# hash-rename
Python script to rename files in a folder using a hash function.

usage: renameToHash.py [-h] [-s HASH] [-r REGEX] path

script to batch rename files in a folder to hashnames

positional arguments:
  path                  path to the directory for hash rename, use '.' for cwd

optional arguments:
  -h, --help            show this help message and exit
  -s HASH, --hash HASH  hash method [md5|sha1|sha224|sha256|sha384|sha512]
  -r REGEX, --regex REGEX
                        file types separated by | (e.g.: jpg|png)
