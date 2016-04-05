#!/usr/bin/env python


# <add_underscore.py, replace spaces in fasta header by underscores>
# Copyright (C) <2016>  <Shengwei Hou> <housw2010'at'gmail'dot'com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import fileinput
import argparse


def replaceAll(path2file, old, new):
    """
    :param path2file: file to be operate on
    :param old:       string to be replaced
    :param new:       string to replace
    :return:          None

    replace 'old' with 'new' in path2file inplace

    """
    # with inplace=1, assign input file to stdout
    for line in fileinput.input(path2file, inplace=1):
        if old in line:
            if line.startswith(">"):
                line = line.replace(old, new)
        sys.stdout.write(line)


def main():

    # parse arguments
    parser = argparse.ArgumentParser(description="replace spaces in fasta header by underscores")
    parser.add_argument("input", help="input fasta file or folder contains fasta files")
    parser.add_argument("-r", "--reverse", action="store_true", default=False, help="reverse operation, "
                                                                                    "replace all underscores by spaces")
    args = parser.parse_args()

    # replace spaces by underscores or vice versa
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



