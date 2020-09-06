#!/usr/bin/env python3
"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from tests.icite import ICiteTester


def test_print_paper():
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""
    pmid = 22882545

    # Clean iCite files
    obj = ICiteTester()
    obj.rm_icitefiles()

    # iCite files are downloaded with the first call
    obj.get_paper(pmid, force_download=False)
    f2mtime = obj.get_f2mtime(min_files=50)

    # iCite files are imported (NOT downloaded) with the second call
    obj.get_paper(pmid, force_download=False)
    assert obj.get_f2mtime(min_files=50) == f2mtime, 'iCite FILES SHOULD NOT HAVE BE MODIFIED'

    # Clean iCite files
    obj.rm_icitefiles()


if __name__ == '__main__':
    test_print_paper()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
