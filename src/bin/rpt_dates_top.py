#!/usr/bin/env python3
"""Given a user query, query PubMed and return PMIDs. Then run NIH's iCite on the PMIDs"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cli.rptdatestop import RptDatesTop


def main():
    """Download PMIDs returned from user queries. Write: ./log/pmids ./log/icite"""
    obj = RptDatesTop()
    obj.cli()


if __name__ == '__main__':
    main()

# Copyright (C) 2020-present DV Klopfenstein. All rights reserved.
