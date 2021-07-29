#!/usr/bin/env python3
"""Download over 100,000 PMIDs to be used in testing"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import argv
from os.path import exists
from timeit import default_timer
import tracemalloc
from tests.icite import prt_hms
from tests.icite import get_dnld_files
from tests.icite import get_filename_test
from tests.icite import get_filename_testdata


def main():
    """Download over 100,000 PMIDs to be used in testing"""
    force_dnld = len(argv) != 1

    # Files from: https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
    fins_dnld = get_dnld_files(r'pubmed*.xml')
    pmids = _read_pmids(fins_dnld)

    # Save PMIDs into a Python module
    file_py = get_filename_test('pmids_many.py')
    file_txt = get_filename_testdata('pmids_many.txt')
    if len(pmids) > 100000:
        _write_pmids_py(file_py, pmids, force_dnld)
        _write_pmids_txt(file_txt, pmids, force_dnld)
        from tests.pmids_many import PMIDS
        print('{N:,} PMIDs IMPORTED: {PY}'.format(N=len(PMIDS), PY=file_py))
    else:
        print('NOT ENOUGH PMIDS TO WRITE {F}'.format(F=file_py))

def _write_pmids_py(fout_py, pmids, force_dnld):
    """Write PMIDs to a Python test module"""
    docstr = '"""{N} PMIDs downloaded from https://ftp.ncbi.nlm.nih.gov/pubmed/baseline"""\n\n'
    if not exists(fout_py) or force_dnld:
        tic = default_timer()
        with open(fout_py, 'w') as prt:
            prt.write(docstr.format(N=len(pmids)))
            prt.write('# Created with: $ src/tests/dnld_pmids_100k.py dnld\n\n')
            prt.write('# pylint: disable=too-many-lines\n')
            prt.write('PMIDS = [\n')
            for pmid in pmids:
                prt.write('    {PMID},\n'.format(PMID=pmid))
            prt.write(']\n')
        prt_hms(tic, '  WROTE {N:,} PMIDs: {PY}'.format(N=len(pmids), PY=fout_py))
    else:
        print('NOT OVERWRITING {F}'.format(F=fout_py))

def _write_pmids_txt(fout_py, pmids, force_dnld):
    """Write PMIDs to a Python test module"""
    fout_txt = fout_py.replace('py', 'txt')
    docstr = '# {N} PMIDs downloaded from https://ftp.ncbi.nlm.nih.gov/pubmed/baseline\n\n'
    if not exists(fout_txt) or force_dnld:
        tic = default_timer()
        with open(fout_txt, 'w') as prt:
            prt.write(docstr.format(N=len(pmids)))
            prt.write('# Created with: $ src/tests/dnld_pmids_100k.py dnld\n\n')
            for pmid in pmids:
                prt.write('{PMID}\n'.format(PMID=pmid))
        prt_hms(tic, '  WROTE {N:,} PMIDs: {PY}'.format(N=len(pmids), PY=fout_txt))
    else:
        print('NOT OVERWRITING {F}'.format(F=fout_txt))

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

def _get_traced_memory():
    """Run example of tracking memory used by this script"""
    tic = default_timer()
    tracemalloc.start()
    main()
    prt_hms(tic, "Current: %d, Peak %d" % tracemalloc.get_traced_memory())


if __name__ == '__main__':
    main()
    #_get_traced_memory()

# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
