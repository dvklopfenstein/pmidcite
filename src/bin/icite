#!/usr/bin/env python3
"""Given a PubMed ID (PMID), return a list of citing publications"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cli.icite import NIHiCiteCli  # get_argparser
from pmidcite.cfg import get_cfgparser
from pmidcite.icite.run import PmidCite


def main():
    """Print lists of pubs in formation"""
    NIHiCiteCli(PmidCite(get_cfgparser())).cli()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
