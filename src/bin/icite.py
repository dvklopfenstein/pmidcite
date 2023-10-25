#!/usr/bin/env python3
"""Given a PubMed ID (PMID), return a list of citing publications"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from pmidcite.cli.icite import NIHiCiteCli  # get_argparser
from pmidcite.cfg import get_cfgparser


def main():
    """Print lists of pubs in formation"""
    NIHiCiteCli(get_cfgparser(prt=None)).cli()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
