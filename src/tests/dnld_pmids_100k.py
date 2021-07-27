#!/usr/bin/env python3
"""Download over 100,000 PMIDs to be used in testing"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import argv
from os.path import exists
from timeit import default_timer
from tests.icite import prt_hms
from tests.icite import get_dnld_files
from tests.icite import get_filename_test


def main():
    """Download over 100,000 PMIDs to be used in testing"""
    force_dnld = len(argv) != 1

    # Files from: https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
    fins_dnld = get_dnld_files(r'pubmed*.xml')
    pmids = _read_pmids(fins_dnld)

    # Save PMIDs into a Python module
    file_py = get_filename_test('pmids_many.py')
    if len(pmids) > 100000:
        _write_pmids(file_py, pmids, force_dnld)
        from tests.pmids_many import PMIDS
        print('{N:,} PMIDs IMPORTED: {PY}'.format(N=len(PMIDS), PY=file_py))
    else:
        print('NOT ENOUGH PMIDS TO WRITE {F}'.format(F=file_py))

def _write_pmids(file_py, pmids, force_dnld):
    """Write PMIDs to a Python test module"""
    docstr = '"""{N} PMIDs downloaded from https://ftp.ncbi.nlm.nih.gov/pubmed/baseline"""\n\n'
    if not exists(file_py) or force_dnld:
        with open(file_py, 'w') as prt:
            prt.write(docstr.format(N=len(pmids)))
            prt.write('# Created with: $ src/tests/dnld_pmids_100k.py dnld\n\n')
            prt.write('# pylint: disable=too-many-lines\n')
            prt.write('PMIDS = [\n')
            for pmid in pmids:
                prt.write('    {PMID},\n'.format(PMID=pmid))
            prt.write(']\n')
        print('  WROTE {N:,} PMIDs: {PY}'.format(N=len(pmids), PY=file_py))
    else:
        print('NOT OVERWRITING {F}'.format(F=file_py))

def _read_pmids(xmls):
    """Read PMIDs from XML files"""
    pmids_all = set()
    tic0 = default_timer()
    for fin in xmls:
        tic = default_timer()
        with open(fin) as ifstrm:
            pmids_cur = set()
            for line in ifstrm:
                if 'PMID' in line:
                    pt0 = line.find(">")
                    if pt0 != -1:
                        pt1 = line.find('</PMID>')
                        if pt1 != -1:
                            pmids_cur.add(int(line[pt0+1:pt1]))
            tic = prt_hms(tic, '{N:7,} PMIDs READ: {F}'.format(N=len(pmids_cur), F=fin))
            pmids_all.update(pmids_cur)
    prt_hms(tic0, '{N:7,} PMIDs READ'.format(N=len(pmids_all)))
    return pmids_all


if __name__ == '__main__':
    main()

# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
