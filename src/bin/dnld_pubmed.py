#!/usr/bin/env python3
"""Given a PubMed ID (PMID), download its record from PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cli.dnldpubmed import DnldPubMed  # get_argparser


def main():
    """Given a PubMed ID (PMID), download its record from PubMed"""
    # PubMed records include the abstract, list of authors, journal, etc.
    DnldPubMed().cli()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
