#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Transform a sessionfile from original format to ReadSession.statusToString format
arguments (mandatory):
    orig_file : source file, in the original format
    dest_file : destination file, in the new format
"""
import argparse
import os
from os import path
import sys

from ReadSession import readsession


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=globals()['__doc__'], add_help=True)
    parser.add_argument('orig_file')
    parser.add_argument('dest_file')

    args = parser.parse_args()

    print('called with: original={} and destination={}'.format(args.orig_file, args.dest_file))

    if not path.isfile(args.orig_file):
        print('orig_file=({}) is not a valid file.'.format(args.orig_file))

    with open(args.dest_file, 'w') as df:
        def writesession(iid, bookOrder):
            df.write(bookOrder.statusToString())
            df.write(os.linesep)
        readsession(args.orig_file,callback=writesession)
