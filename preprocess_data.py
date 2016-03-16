import cPickle
import numpy as np

def load_session(session_file):
    with open(session_file, 'r') as f:
        data = cPickle.load(f)

    ts = data[:, 1]
    last = data[:, 4]
    # remove rows where last (price) is 0, last is column 4
    data = data[data[:,4]!=0]

    return data
