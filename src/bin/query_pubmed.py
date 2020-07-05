#!/usr/bin/env python3
"""Given a PubMed query, retrun the pubmed IDs"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cli.querypubmed import QueryPubMed  # get_argparser


def main():
    """Given a PubMed query, retrun the pubmed IDs"""
    QueryPubMed().cli()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
