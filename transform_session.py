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

import numpy as np

from ReadSession import readsession


def transform_session_to_file(orig_file, dest_file):
    with open(dest_file, 'w') as df:

        def writesession(iid, bookOrder):
            df.write(bookOrder.statusToString())
            df.write(os.linesep)

        readsession(orig_file, callback=writesession)


def add_session_to_list(orig_file, ses_list):
    def append_orders_to_list(iid, bookOrder):
        print('bookOrder:', bookOrder.id, bookOrder.lastPrice)
        ses_list.append(bookOrder.toList())

    readsession(orig_file, callback=append_orders_to_list)
    return ses


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=globals()['__doc__'], add_help=True)
    parser.add_argument('orig_file')
    parser.add_argument('--out', dest='output', default='file', choices=['file', 'numpy'])

    args = parser.parse_args()

    orig_file = args.orig_file
    dest_file = orig_file+'.out'

    print('called with: original={} and output={}'.format(orig_file, args.output))

    if not path.isfile(orig_file):
        print('orig_file=({}) is not a valid file.'.format(orig_file))

    if args.output == 'numpy':
        session_list = []
        session_list = add_session_to_numpy_arr(orig_file, session_list)
        numpy.array(session_list)
    else:
        transform_session_to_file(orig_file, dest_file)
