"""Read a file created by pmidcite and write simple text file of PMIDs"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys


def read_pmids(fin, prt=sys.stdout):
    """Read PMIDs from a file. One PMID per line."""
    pmids = []
    with open(fin) as ifstrm:
        for line in ifstrm:
            line = line.strip()
            if line.isdigit():
                pmids.append(int(line))
        if prt:
            prt.write('{N:6,} PMIDs READ: {FILE}\n'.format(N=len(pmids), FILE=fin))
    return pmids

def get_pmids(pmid_list, fin_pmids):
    """Get PMIDs from the command line or from a file"""
    if not pmid_list and not fin_pmids:
        return []
    pmids = list(pmid_list)
    # Search PMIDs listed in files
    seen = set(pmids)
    if fin_pmids:
        for fin in fin_pmids:
            if os.path.exists(fin):
                for pmid in read_pmids(fin):
                    if pmid not in seen:
                        pmids.append(pmid)
            else:
                print('  MISSING: {FILE}'.format(FILE=fin))
    return pmids

def read_top_pmids(pmidcite_txt, top='TOP'):
    """Get PMIDs already found in pmidcite.txt"""
    pmids = set()
    with open(pmidcite_txt) as ifstrm:
        topstr = '{TOP} '.format(TOP=top)
        toplen = len(topstr)
        for line in ifstrm:
            if line[:toplen] == topstr:
                flds = line.split()
                assert flds[1].isdigit(), '{} {}'.format(pmidcite_txt, flds)
                pmids.add(int(flds[1]))
    return pmids

def wr_pmids(fout_txt, pmids, mode='w', log=sys.stdout):
    """Write PMIDs into a text file, one PMID per line"""
    with open(fout_txt, mode) as prt:
        for pmid in pmids:
            prt.write('{PMID}\n'.format(PMID=pmid))
        if log:
            log.write('{N:6,} WROTE: {FOUT}\n'.format(N=len(pmids), FOUT=fout_txt))

def mk_outname_pmids(fin):
    """Given input file, return output file for PMIDs"""
    outdir, outname = os.path.split(fin)
    basename, ext = os.path.splitext(outname)
    return os.path.join(outdir, '{BASE}_pmids{EXT}'.format(BASE=basename, EXT=ext))

def get_outfile(outfile, append_outfile, force_write):
    """Given arguments, return outfile"""
    mode, force_wr = _get_mode_force(outfile, force_write, append_outfile)
    return {
        'outfile': _get_outfile_resolved(outfile, append_outfile),
        'mode':mode,
        'force_write':force_wr}

def _get_mode_force(outfile, force_write, append_outfile):
    """Given arguments, return outfile"""
    # if '-o', only over-write existing file if explicitly requested
    if outfile is not None:
        return 'w', force_write
    # if '-a', always append given file or create the file if needed
    if append_outfile is not None:
        return 'a', True
    return 'w', True

def _get_outfile_resolved(outfile, append_outfile):
    """Given outfile (write_outfile) and append_outfile, return one resolved outfile name"""
    if outfile is not None:
        return outfile
    if append_outfile is not None:
        return append_outfile
    return None


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
