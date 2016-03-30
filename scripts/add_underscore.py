#!/usr/bin/python

import sys
import os
import fileinput
import argparse

def replaceAll(path2file,old,new):
    """ replace 'old' with 'new' in path2file inplace
    """
    # with inplace=1, assign input file to stdout
    for line in fileinput.input(path2file, inplace=1):
        if old in line:
            line = line.replace(old,new)
        sys.stdout.write(line)




def main():

    # parse arguments
    parser = argparse.ArgumentParser(description="replace spaces in fasta header by underscores")
    parser.add_argument("input", help="input fasta file or folder contains fasta files")
    parser.add_argument("-r", "--reverse", action="store_true", default=False, help="reverse operation, replace all underscores by spaces")
    args = parser.parse_args()

    #
    if os.path.isdir(args.input):
        for f in os.listdir(args.input):
            if f.endswith(".fasta") or f.endswith(".fna") or f.endswith(".fa"):
                if args.reverse:
                    replaceAll(os.path.join(args.input, f), "_", " ")
                else:
                    replaceAll(os.path.join(args.input, f), " ", "_")
    else:
        if args.reverse:
            replaceAll(args.input, "_", " ")
        else:
            replaceAll(args.input, " ", "_")



if __name__ == "__main__":
    main()



