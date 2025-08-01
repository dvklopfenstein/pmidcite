#!/usr/bin/env python3
"""ASCII scatter plot adapted from https://github.com/dzerbino/ascii_plots"""

__copyright__ = "Copyright (C) 2013, Authored by Daniel Zerbino. All rights reserved."
__copyright__ = "Copyright (C) 2020, Adapted by DV Klopfenstein, PhD. All rights reserved."

from pmidcite.plot.scatter import AsciiScatter


def main():
    """ASCII scatter plot adapted from https://github.com/dzerbino/ascii_plots"""
    obj = AsciiScatter()
    xydata = obj.read_stdin_ints()
    obj.run(xydata)


if __name__ == '__main__':
    main()

# Copyright (C) 2020 DV Klopfenstein, PhD. All rights reserved.
