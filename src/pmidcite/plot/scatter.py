"""ASCII scatter plot adapted from https://github.com/dzerbino/ascii_plots"""

__copyright__ = "Copyright (C) 2013-present, Authored by Daniel Zerbino. All rights reserved."
__copyright__ = "Copyright (C) 2020-present, Adapted by DV Klopfenstein. All rights reserved."

import sys
from os import environ
import locale
locale.setlocale(locale.LC_ALL, '')


class AsciiScatter:
    """ASCII scatter plot adapted from https://github.com/dzerbino/ascii_plots"""

    scale = r' .\'\`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    scale_range = len(scale) - 1

    width = int(environ['COLUMNS']) if 'COLUMNS' in environ else 80

    def _asciify(self, val, max_val):
        #return str(int(self.scale_range * val / max_val))
        return self.scale[int(self.scale_range * val / max_val)]

    def _asciifyline(self, line, max_val):
        return map(lambda val: self._asciify(val, max_val), line)

    def _asciifyarray(self, array, max_val, min_x, max_x, min_y, max_y):
        width = self.width
        print("".join("-" for i in range(width + 2)) + " " + str(max_y))
        for line in array:
            print('|' + ''.join(self._asciifyline(line, max_val)) + "|")
        print("".join("-" for i in range(width + 2)) + " " + str(min_y))
        print("%-10.6f" % min_x + "".join(" " for i in range(width + 2 - 20)) + "%10.6f" % max_x)

    def _empty_line(self):
        return [0 for i in range(self.width)]

    def _empty_array(self):
        return [self._empty_line() for i in range(self.width//3)]

    def run(self):
        pairs = []
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for line in sys.stdin:
            try:
                xval, yval = map(locale.atof, line.strip().split())
            except RuntimeError:
                continue

            if xval == locale.atof("Inf") or yval == locale.atof("Inf"):
                continue
            if xval == locale.atof("-Inf") or yval == locale.atof("-Inf"):
                continue

            if min_x is None or xval < min_x:
                min_x = xval
            if min_y is None or yval < min_y:
                min_y = yval
            if max_x is None or xval > max_x:
                max_x = xval
            if max_y is None or yval > max_y:
                max_y = yval
            pairs.append((xval, yval))

        span_x = max_x - min_x
        span_y = max_y - min_y
        max_val = None
        array = self._empty_array()
        for X, Y in pairs:
            scaled_x = int((self.width - 1) * (X - min_x) / span_x)
            scaled_y = int((self.width//3 - 1) * (max_y - Y) / span_y)
            array[scaled_y][scaled_x] += 1
            if max_val is None or array[scaled_y][scaled_x] > max_val:
                max_val = array[scaled_y][scaled_x]

        self._asciifyarray(array, max_val, min_x, max_x, min_y, max_y)


# Copyright (C) 2013-present, Authored by Daniel Zerbino. All rights reserved.
# Copyright (C) 2020-present, Adapted for pmidcite by DV Klopfenstein. All rights reserved.
