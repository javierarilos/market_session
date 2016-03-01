"""
Read a Session, with file format:
    First line is date and time:
        # 20100222 07:55:00
    Every other line is:
        iid, offset (in ms since MIDNIGHT), entry
            e.g.     F:FSTXH0|28641500|l2505v0V0
        entries:
            Tick (last): id,offs, l<LAST>v<LASTVOL>V<TOTVOL>
                F:FESXH0|28797157|l2788v38V5216
            nb: nbids
            na: nasks
            b0, ... b9: bids (B=10+) bid price
            u/U: bid volume
            a/A: ask price
            w/W: ask vol
"""

import time


class BookOrder:
    def __init__(self, id):
        self.id = id
        self.nbids = 0
        self.nasks = 0
        self.askPrices = [0]*30  # todo fill the array
        self.bidPrices = [0]*30
        self.askVolumes = [0]*30
        self.bidVolumes = [0]*30
        self.lastPrice = 0
        self.lastVolume = 0
        self.totalVolume = 0
        self.timestamp = ""

    def increment(self, entry, timestamp):
        self.timestamp = timestamp  # in milliseconds
        idx = 0
        state = 0  # 0=code, 1=number
        code = ''
        number = ''
        entries = []
        while idx <= len(entry):
            if idx < len(entry):
                c = entry[idx]
            else:
                c = '!'  # end marker
            if c == ',':
                c = '.'
            if state == 0:
                if c.isdigit() or c == '.':
                    number = c
                    state = 1
                else:
                    code += c
            elif state == 1:
                if c.isdigit() or c == '.':
                    number += c
                else:
                    entries.append((code, number))
                    code = c
                    state = 0
            idx += 1
        # Reconstruct state of order book
        # Bugs in writesession: p < 0: B is used for 9 already
        # numbers formatted with , instead of .
        for code, value in entries:
            try:
                if code == 'nb':
                    self.nbids = int(value)
                elif code == 'na':
                    self.nasks = int(value)
                elif code == 'b':
                    self.bidPrices[int(value[0:1])] = float(value[1:])
                elif code == 'a':
                    self.askPrices[int(value[0:1])] = float(value[1:])
                elif code == 'u':
                    self.bidVolumes[int(value[0:1])] = int(value[1:])
                elif code == 'w':
                    self.askVolumes[int(value[0:1])] = int(value[1:])
                elif code == 'l':
                    self.lastPrice = float(value)
                elif code == 'v':
                    self.lastVolume = int(value)
                elif code == 'V':
                    self.totalVolume = int(value)
                # else:
                #   print "WTF is code", code, "line=", line
            except:
                print code, value, line
                return

    def statusToString(self):
        """ Status to String in the format, all in a single line:
            <id>|
            <timestamp>|
            nb<nbids>
            na<nasks>
            b<bid>
            [b{0,9}<bid-n>u{0,9}<bidVolume-n>]*
            [a{0,9}<ask-n>w{0,9}<askVolume-n>]*
            l<last>
            v<lastVolume>
            V<volume>
        """
        pref = "nb{}na{}".format(self.nbids, self.nasks)
        for idx in range(self.nbids):
            pref += "b{}{}u{}{}".format(idx, self.bidPrices[idx], idx, self.bidVolumes[idx])
        for idx in range(self.nasks):
            pref += "a{}{}w{}{}".format(idx, self.askPrices[idx], idx, self.askVolumes[idx])
        pref += ("l{}v{}V{}".format(self.lastPrice, self.lastVolume, self.totalVolume))
        return pref

    def toString(self):
        return "{}|{}|{}".format(self.id, self.timestamp, self.statusToString())


def readsession(fn, callback=None):
    f = open(fn)
    t0 = 0

    instruments = {}

    for line in f.readlines():
        if line[0] == '#':
            date = line[2:].split(' ')[0]
            continue
        # Interpret each line
        (iid, offs, entry) = line.split('|')
        if iid not in instruments:
            instruments[iid] = BookOrder(iid)
        bookOrder = instruments[iid]

        t = int(offs)  # in milliseconds
        if t0 == 0:
            t0 = t

        bookOrder.increment(entry, t)

        if callback:
            callback(iid, bookOrder)
