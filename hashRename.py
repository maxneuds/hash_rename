#!/bin/python
import os
import argparse
import hashlib
import re

##########
# main
##########

def main():
    # get args
    args = parse_args()
    # get path
    sPath = get_path(args.path)
    # rename files in path by hash
    h = dict_hash_methods[args.hash]
    hash_dir(sPath, h, args.regex)

##########
# dicts
##########

dict_hash_methods = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
}

##########
# methods
##########

def parse_args():
    desc_args = "script to batch rename files in a folder to hashnames"
    parser = argparse.ArgumentParser(
        description=desc_args
    )

    help_path = "path to the directory for hash rename, use '.' for cwd"
    parser.add_argument(
        "path",
        help=help_path,
    )

    help_hash = "hash method [md5|sha1|sha224|sha256|sha384|sha512]"
    parser.add_argument(
        "-s", "--hash",
        help=help_hash,
        default="md5",
    )

    help_re = "file types separated by | (e.g.: jpg|png)"
    parser.add_argument(
        "-r", "--regex",
        help=help_re,
    )

    args = parser.parse_args()
    return args

def get_path(path):
    sPath = os.path.abspath(path)
    if os.path.exists(sPath):
        return sPath
    else:
        print("invalid path!")
        exit()

def get_hash_method(method):
    if method in dict_hash_methods:
        h = dict_hash_methods[method]
        return h
    else:
        print("invalid hash algorithm!")
        print("use: md5, sha1, sha224, sha256, sha384, sha512")
        exit()

def hash_dir(sPath, h, regex):
    flist = os.listdir(sPath)
    # filter: files only
    flist = [f for f in flist if os.path.isfile(f)]
    # filter: no dotfiles
    pattern = r"^[^\.].*$"
    flist = [f for f in flist if re.match(pattern, f)]
    # filter filetypes for regex
    if regex is not None:
        pattern = rf"^[^\.].*\.({regex})$"
        flist = [f for f in flist if re.match(pattern, f)]
    for f in flist:
        print(f)
    # sort list by name... just because we can.
    flist = sorted(flist, key=str.lower)
    for f in flist:
        with open(f, "rb") as file:
            hname = h(file.read()).hexdigest()
        print(f"trying to rename: {f}")
        fext = os.path.splitext(f)[1]
        newname = hname + fext
        # skip files already with hash name
        if f == newname:
            print(" -> file already hash named!")
        else:
            # remove duplicates
            if os.path.isfile(newname):
                try:
                    print(f" -> removing duplicate: {f}")
                    os.remove(f)
                    print(f" -> removed: {f}")
                except Exception as e:
                    print(" -> couldn't remove duplicate")
            else:
                try:
                    # rename to hash name
                    os.rename(f, newname)
                    print(f" -> {newname}")
                except Exception as e:
                    print(f" -> couldn't rename: {f}")

if __name__ == "__main__":
    main()
