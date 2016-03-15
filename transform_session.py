#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Transform a sessionfile from original format to ReadSession.statusToString format
arguments (mandatory):
    session_file : source file, in the original format
    dest_file : destination file, in the new format
"""
import argparse
import os
from os import path
import sys
import cPickle as pickle

import numpy as np

from ReadSession import readsession


def transform_session_to_file(session_file, dest_file, filter_iid=None):
    with open(dest_file, 'w') as df:

        def writesession(iid, bookOrder):
            df.write(bookOrder.statusToString())
            df.write(os.linesep)

        readsession(session_file, callback=writesession, filter_iid=filter_iid)


def add_session_to_list(session_file, ses_list, filter_iid=None):
    def append_orders_to_list(iid, bookOrder):
        ses_list.append(bookOrder.toList())

    readsession(session_file, callback=append_orders_to_list, filter_iid=filter_iid)
    return ses_list


def transform_session_to_numpy(session_files, filter_iid=None):
    session_list = []
    nr = 0
    import time
    start = time.time()
    for session_file in session_files:
        if not path.isfile(session_file):
            print('ERROR: session_file=({}) is not a valid file. Exiting.'.format(session_file))
            sys.exit(1)

        session_list = add_session_to_list(session_file, session_list, filter_iid=filter_iid)

    session_np = np.array(session_list)

    with open('sessions.pkl', 'w') as f:
        pickle.dump(session_np, f)
    print('')
    print('--> DONE. session rows={} total time={}'.format(len(session_np), time.time() - start))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=globals()['__doc__'], add_help=True)
    parser.add_argument('session_files', nargs='+')
    parser.add_argument('--out', dest='output', default='file', choices=['file', 'numpy'])
    parser.add_argument('--instrument', dest='instrument', default=None)

    args = parser.parse_args()

    session_files = args.session_files
    output = args.output

    print('Transforming sessions: session_files={} and output={}'.format(session_files, output))

    if output == 'numpy':
        r = transform_session_to_numpy(session_files, filter_iid=args.instrument)
        sys.exit(r)
    elif output == 'file':
        for session_file in args.session_files:
            if not path.isfile(session_file):
                print('session_file=({}) is not a valid file.'.format(session_file))
                sys.exit(1)

            dest_file = session_file+'.out'
            transform_session_to_file(session_file, dest_file, filter_iid=args.instrument)
