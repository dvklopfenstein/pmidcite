#!/usr/bin/env python3
"""Given a PubMed ID (PMID), return a list of citing publications"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cli.icite import NIHiCiteArgs  # get_argparser


def main():
    """Print lists of pubs in formation"""
    argobj = NIHiCiteArgs()
    argobj.run()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.