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

    scale = r' 123456789abcdef!@#$%^&*(ABCDEFGHIJKLMNOPQRSTUVWXYZ-=_+{}[]|\:";<>,./?'

    def __init__(self, maxwidth=100):
        self.maxwidth = maxwidth

    def run(self, xydata):
        """Create an ASCII plot, given XY data"""
        minmax = self._get_minmax(xydata)
        cnts_2d = self._get_xy_scaled(xydata, **minmax)
        letter2cnt = self._asciifyarray(cnts_2d, **minmax)
        self._prt_key(letter2cnt)

    @staticmethod
    def read_stdin_ints():
        """Get (x, y) points from stdin"""
        xydata = []
        for line in sys.stdin:
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
                scale_idx = cnt%scale_range
                letter = scale[scale_idx]
                letter2cnt[letter] = cnt
                chrs_1d.append(letter)
            chrs_2d.append(chrs_1d)
        return {'chrs_2d':chrs_2d, 'letter2cnt':letter2cnt}

    def _get_width(self, span_x):
        """Given the time span for citations, return width of ASCII graph"""
        multiplier = self.maxwidth//span_x
        return span_x*multiplier

    def _asciifyarray(self, array_2d, width, **kws):
        min_x, max_x, min_y, max_y, span_x = [kws[k] for k in ['min_x', 'max_x', 'min_y', 'max_y', 'span_x']]
        max_val = max(chain(*array_2d))
        print("".join("-" for i in range(width + 2)) + " " + str(max_y))
        dct = self._asciify_2d(array_2d, max_val)
        for chrs_1d in dct['chrs_2d']:
            print('|' + ''.join(chrs_1d) + "|")
        print("".join("-" for i in range(width + 2)) + " " + str(min_y))
        print(str(min_x) + " "*width + str(max_x))
        return dct['letter2cnt']

    def _prt_key(self, letter2cnt, prt=sys.stdout):
        """Print the counts and the letter that represents it"""
        for letter, cnt in sorted(letter2cnt.items(), key=lambda t: t[1]):
            if cnt != 0 and letter != str(cnt):
                prt.write('{A} {N}'.format(A=letter, N=cnt))

    def _get_xy_scaled(self, xydata, width, **kws):
        """Scale XY values to fit in ASCII width"""
        min_x, max_y, span_x, span_x, span_y = [kws[k] for k in ['min_x', 'max_y', 'span_x', 'span_x', 'span_y']]
        array = [[0]*width for i in range(width//3)]
        for xval, yval in sorted(xydata, key=lambda t: t[0]):
            pos_x = int(round((width - 1) * (xval - min_x) / span_x))
            pos_y = int(round((width//3 - 1) * (max_y - yval) / span_y))
            array[pos_y][pos_x] += 1
            ## print('X({}) Y({:3}) -> {} {:2} VALUE {}'.format(xval, yval, pos_x, pos_y, array[pos_y][pos_x]))
        return array

    def _get_minmax(self, xydata):
        """Get min and max data from XY xydata"""
        if not xydata:
            return {}
        xvals, yvals = zip(*xydata)
        min_x = min(xvals)
        max_x = max(xvals)
        min_y = min(yvals)
        max_y = max(yvals)
        span_x = max_x - min_x
        return {
            'min_x': min_x, 'max_x': max_x, 'span_x': span_x,
            'min_y': min_y, 'max_y': max_y, 'span_y': max_y - min_y,
            'width': self._get_width(span_x),
        }


# Copyright (C) 2013-present, Authored by Daniel Zerbino. All rights reserved.
# Copyright (C) 2020-present, Adapted for pmidcite by DV Klopfenstein. All rights reserved.
