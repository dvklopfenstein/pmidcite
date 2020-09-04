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

    scale = r' .\'\`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    scale_range = len(scale) - 1

    def __init__(self, width=80):
        self.width = width

    def _asciify(self, val, max_val):
        #return str(int(self.scale_range * val / max_val))
        return self.scale[int(self.scale_range * val / max_val)]

    def _asciifyline(self, line, max_val):
        return map(lambda val: self._asciify(val, max_val), line)

    def _asciifyarray(self, array, **kws):
        width = self.width
        min_x, max_x, min_y, max_y = [kws[k] for k in ['min_x', 'max_x', 'min_y', 'max_y']]
        max_val = max(chain(*array))
        print("".join("-" for i in range(width + 2)) + " " + str(max_y))
        for line in array:
            print('|' + ''.join(self._asciifyline(line, max_val)) + "|")
        print("".join("-" for i in range(width + 2)) + " " + str(min_y))
        print("%-10.6f" % min_x + "".join(" " for i in range(width + 2 - 20)) + "%10.6f" % max_x)

    def run(self, xydata):
        """Create an ASCII plot, given XY data"""
        minmax = self._get_minmax(xydata)
        txtdata = self._get_xy_scaled(xydata, **minmax)
        self._asciifyarray(txtdata, **minmax)

    @staticmethod
    def read_stdin_floats():
        """Get (x, y) points from stdin"""
        xydata = []
        for line in sys.stdin:
            try:
                xval, yval = map(locale.atof, line.strip().split())
            except RuntimeError:
                continue

            if xval == locale.atof("Inf") or yval == locale.atof("Inf"):
                continue
            if xval == locale.atof("-Inf") or yval == locale.atof("-Inf"):
                continue
            xydata.append((xval, yval))
        return xydata

    def _get_xy_scaled(self, xydata, **kws):
        """Scale XY values to fit in ASCII width"""
        width = self.width
        min_x, max_y, span_x, span_y = [kws[k] for k in ['min_x', 'max_y', 'span_x', 'span_y']]
        array = [[0]*width for i in range(width//3)]
        for xval, yval in xydata:
            scaled_x = int((width - 1) * (xval - min_x) / span_x)
            scaled_y = int((width//3 - 1) * (max_y - yval) / span_y)
            array[scaled_y][scaled_x] += 1
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
