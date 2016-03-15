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
            l<lastPrice>
            v<lastVolume>
            V<volume>
            [b{0,9}<bid-n>u{0,9}<bidVolume-n>]*
            [a{0,9}<ask-n>w{0,9}<askVolume-n>]*
        """
        pref = "nb{}na{}".format(self.nbids, self.nasks)
        pref += ("l{}v{}V{}".format(self.lastPrice, self.lastVolume, self.totalVolume))
        for idx in range(self.nbids):
            pref += "b{}{}u{}{}".format(idx, self.bidPrices[idx], idx, self.bidVolumes[idx])
        for idx in range(self.nasks):
            pref += "a{}{}w{}{}".format(idx, self.askPrices[idx], idx, self.askVolumes[idx])
        return pref

    def toString(self):
        return "{}|{}|{}".format(self.id, self.timestamp, self.statusToString())

    def toList(self):
        """returns a list:
            [
                hash(id), timestamp, nbids, nasks,
                l, v, V,
                b0, u0 ..., b20, u29,
                a0, w0 ..., a29, w29,
            ]
        """
        tmp_list = [
                    hash(self.id), self.timestamp, self.nbids, self.nasks,
                    self.lastPrice, self.lastVolume, self.totalVolume
        ]

        for b, u in zip(self.bidPrices, self.bidVolumes):
            tmp_list.append(b)
            tmp_list.append(u)
        for a, w in zip(self.askPrices, self.askVolumes):
            tmp_list.append(a)
            tmp_list.append(w)
        return tmp_list

    def getListNames(self):
        names = [
                    'id_hash', 'timestamp', 'nbids', 'nasks',
                    'l', 'v', 'V'
        ]
        for i in range(30):
            names.append('b'+str(i))
            names.append('u'+str(i))
        for i in range(30):
            names.append('a'+str(i))
            names.append('w'+str(i))
        return names


def readsession(fn, callback=None, filter_iid=None):
    f = open(fn)
    t0 = 0

    instruments = {}

    for line in f.readlines():
        if line[0] == '#':
            date = line[2:].split(' ')[0]
            continue
        # Interpret each line
        (iid, offs, entry) = line.split('|')
        if not filter_iid or (filter_iid and filter_iid == iid):
            if iid not in instruments:
                instruments[iid] = BookOrder(iid)
            bookOrder = instruments[iid]

            t = int(offs)  # in milliseconds
            if t0 == 0:
                t0 = t

            bookOrder.increment(entry, t)

            if callback:
                callback(iid, bookOrder)
