#!/usr/bin/env python3
"""Read a file created by pmidcite and write simple text file of PMIDs"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


from pmidcite.cli.readpmids import ReadPmids  # get_argparser


def main():
    """Print lists of pubs in formation"""
    ReadPmids().cli()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
