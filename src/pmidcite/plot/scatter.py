"""ASCII scatter plot adapted from https://github.com/dzerbino/ascii_plots"""

__copyright__ = "Copyright (C) 2013-present, Authored by Daniel Zerbino. All rights reserved."
__copyright__ = "Copyright (C) 2020-present, Adapted by DV Klopfenstein. All rights reserved."

from itertools import chain
import sys
from collections import Counter
import locale
locale.setlocale(locale.LC_ALL, '')


class AsciiScatter:
    """ASCII scatter plot adapted from https://github.com/dzerbino/ascii_plots"""

    scale = r' 0123456789abcdef!@#$%^&*(ABCDEFGHIJKLMNOPQRSTUVWXYZ-=_+{}[]|\:";<>,./?'

    def __init__(self, width=80):
        self.width = width

    def run(self, xydata):
        """Create an ASCII plot, given XY data"""
        minmax = self._get_minmax(xydata)
        cnts_2d = self._get_xy_scaled(xydata, **minmax)
        self._asciifyarray(cnts_2d, **minmax)

    @staticmethod
    def read_stdin_ints():
        """Get (x, y) points from stdin"""
        xydata = []
        for line in sys.stdin:
            line = line.strip()
            lst = line.split()
            if len(lst) == 2 and lst[0].isdigit() and lst[1].isdigit():
                xydata.append((int(lst[0]), int(lst[1])))
        return xydata

    def _asciify_2d(self, array_2d, max_val):
        chrs_2d = []
        letter2cnt = {}
        scale = self.scale
        scale_range = len(self.scale) - 1
        for array_1d in array_2d:
            chrs_1d = []
            for cnt in array_1d:
                scale_idx = int(scale_range * cnt/ max_val)
                letter = scale[scale_idx]
                letter2cnt[letter] = cnt
                chrs_1d.append(letter)
            chrs_2d.append(chrs_1d)
        return {'chrs_2d':chrs_2d, 'letter2cnt':letter2cnt}

    def _asciifyarray(self, array_2d, **kws):
        width = self.width
        min_x, max_x, min_y, max_y = [kws[k] for k in ['min_x', 'max_x', 'min_y', 'max_y']]
        max_val = max(chain(*array_2d))
        print("".join("-" for i in range(width + 2)) + " " + str(max_y))
        dct = self._asciify_2d(array_2d, max_val)
        for chrs_1d in dct['chrs_2d']:
            print('|' + ''.join(chrs_1d) + "|")
        print("".join("-" for i in range(width + 2)) + " " + str(min_y))
        print(str(min_x) + " "*width + str(max_x))
        self._prt_key(dct['letter2cnt'])

    def _prt_key(self, letter2cnt):
        """Print the counts and the letter that represents it"""
        for letter, cnt in sorted(letter2cnt.items(), key=lambda t: t[1]):
            print(letter, cnt)
        ##for letter in self.scale:

    def _get_xy_scaled(self, xydata, **kws):
        """Scale XY values to fit in ASCII width"""
        width = self.width
        min_x, max_y, span_x, span_y = [kws[k] for k in ['min_x', 'max_y', 'span_x', 'span_y']]
        array = [[0]*width for i in range(width//3)]
        for xval, yval in sorted(xydata, key=lambda t: t[0]):
            pos_x = int(round((width - 1) * (xval - min_x) / span_x))
            pos_y = int(round((width//3 - 1) * (max_y - yval) / span_y))
            print('X({}) Y({:3}) -> {} {:2}'.format(xval, yval, pos_x, pos_y))
            array[pos_y][pos_x] += 1
        return array

    @staticmethod
    def _get_minmax(xydata):
        """Get min and max data from XY xydata"""
        if not xydata:
            return {}
        xvals, yvals = zip(*xydata)
        min_x = min(xvals)
        max_x = max(xvals)
        min_y = min(yvals)
        max_y = max(yvals)
        return {
            'min_x': min_x, 'max_x': max_x, 'span_x': max_x - min_x,
            'min_y': min_y, 'max_y': max_y, 'span_y': max_y - min_y,
        }


# Copyright (C) 2013-present, Authored by Daniel Zerbino. All rights reserved.
# Copyright (C) 2020-present, Adapted for pmidcite by DV Klopfenstein. All rights reserved.
