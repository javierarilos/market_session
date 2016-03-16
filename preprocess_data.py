import cPickle
import numpy as np

def load_session(session_file):
    with open(session_file, 'r') as f:
        data = cPickle.load(f)

    # remove rows where last (price) is 0, last is column 4
    data = data[data[:,4]!=0]

    return data

def prepare_feats_labels(data, window=10, label_after=10, label_column=4, overlap=0):
    """ single feature point contains all data for window*ticks.
        do a sliding window to get all features.
        label is the last price (label_after*ticks)later than end of its window.
    """
    total = len(data)
    feats = []
    labels = []
    for x in xrange(0, len(data) - label_after - window, window):
        window_limit = x + window
        label_row = window_limit + label_after - 1
        feature = data[x:window_limit].flatten()
        label = data[label_row][label_column]  # last price is 4th
        feats.append(feature)
        labels.append(label)
    return np.array(feats), np.array(labels)
