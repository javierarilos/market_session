""" Load data from pickle session file, with only one instrument.
    Plot prices after removing zeroes
"""
import matplotlib.pyplot as plt

import preprocess_data

session_file = 'f_mupssan20140901.F:FESXU4.pkl'

mkt = preprocess_data.load_session(session_file)

ts = mkt[:, 1]
last = mkt[:, 4]

plt.plot(ts, last)
plt.show()
