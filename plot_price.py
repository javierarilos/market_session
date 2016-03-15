""" Load data from pickle session file, with only one instrument.
    Plot prices after removing zeroes
"""
import cPickle
import matplotlib.pyplot as plt

session_file = 'f_mupssan20140901.F:FESXU4.pkl'

with open(session_file, 'r') as f:
    mkt = cPickle.load(f)

ts = mkt[:, 1]
last = mkt[:, 4]
print 'remove zeroes from last (price)'
last = filter(None, last)

removed = len(ts) - len(last)

ts = ts[removed:]

plt.plot(ts, last)
plt.show()
