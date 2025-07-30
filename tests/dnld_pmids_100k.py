#!/usr/bin/env python3
"""Download over 100,000 PMIDs to be used in testing"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from sys import argv
from os.path import exists
from timeit import default_timer
import tracemalloc
from tests.prt_hms import prt_hms
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
        # pylint: disable=import-outside-toplevel
        from tests.pmids_many import PMIDS
        print(f'{len(PMIDS):,} PMIDs IMPORTED: {file_py}')
    else:
        print(f'NOT ENOUGH PMIDS TO WRITE {file_py}')

def _write_pmids_py(fout_py, pmids, force_dnld):
    """Write PMIDs to a Python test module"""
    docstr = (f'"""{len(pmids)} PMIDs '
             'downloaded from https://ftp.ncbi.nlm.nih.gov/pubmed/baseline"""\n\n')
    if not exists(fout_py) or force_dnld:
        tic = default_timer()
        with open(fout_py, 'w', encoding='utf-8') as prt:
            prt.write(docstr.format(N=len(pmids)))
            prt.write('# Created with: $ src/tests/dnld_pmids_100k.py dnld\n\n')
            prt.write('# pylint: disable=too-many-lines\n')
            prt.write('PMIDS = [\n')
            for pmid in pmids:
                prt.write(f'    {pmid},\n')
            prt.write(']\n')
        prt_hms(tic, f'  WROTE {len(pmids):,} PMIDs: {fout_py}')
    else:
        print(f'NOT OVERWRITING {fout_py}')

def _write_pmids_txt(fout_py, pmids, force_dnld):
    """Write PMIDs to a Python test module"""
    fout_txt = fout_py.replace('py', 'txt')
    docstr = '# {N} PMIDs downloaded from https://ftp.ncbi.nlm.nih.gov/pubmed/baseline\n\n'
    if not exists(fout_txt) or force_dnld:
        tic = default_timer()
        with open(fout_txt, 'w', encoding='utf-8') as prt:
            prt.write(docstr.format(N=len(pmids)))
            prt.write('# Created with: $ src/tests/dnld_pmids_100k.py dnld\n\n')
            for pmid in pmids:
                prt.write(f'{pmid}\n')
        prt_hms(tic, f'  WROTE {len(pmids):,} PMIDs: {fout_txt}')
    else:
        print(f'NOT OVERWRITING {fout_txt}')

def _read_pmids(xmls):
    """Read PMIDs from XML files"""
    pmids_all = set()
    tic0 = default_timer()
    for fin in xmls:
        tic = default_timer()
        with open(fin, encoding='utf-8') as ifstrm:
            pmids_cur = set()
            for line in ifstrm:
                if 'PMID' in line:
                    pt0 = line.find(">")
                    if pt0 != -1:
                        pt1 = line.find('</PMID>')
                        if pt1 != -1:
                            pmids_cur.add(int(line[pt0+1:pt1]))
            tic = prt_hms(tic, f'{len(pmids_cur):7,} PMIDs READ: {fin}')
            pmids_all.update(pmids_cur)
    prt_hms(tic0, f'{len(pmids_all):7,} PMIDs READ')
    return pmids_all

def _get_traced_memory():
    """Run example of tracking memory used by this script"""
    tic = default_timer()
    tracemalloc.start()
    main()
    prt_hms(tic, f"Current: %d, Peak {tracemalloc.get_traced_memory()}")


if __name__ == '__main__':
    main()
    #_get_traced_memory()

# Copyright (C) 2021-present, DV Klopfenstein, PhD. All rights reserved.
