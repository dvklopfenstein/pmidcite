"""Given a PubMed ID (PMID), return a list of publications which cite it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import os
import collections as cx
import importlib.util

from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper


class NIHiCiteLoader:
    """Manage pubs notes files"""

    def __init__(self, force_dnld, api, rpt_references=False):
        self.rpt_references = rpt_references
        self.dnld_force = force_dnld
        self.dir_dnld = api.dir_dnld  # e.g., ./icite
        self.api = api                # NIHiCiteAPI

    def wr_papers(self, fout_txt, force, pmid2ntpaper, mode='w'):
        """Run iCite for user-provided PMIDs and write to a file"""
        if not pmid2ntpaper:
            return
        pmids_all = pmid2ntpaper.keys()
        pmids_new = pmids_all
        if mode == 'a':
            pmids_new = self._get_new_pmids(fout_txt, pmids_all)
        if pmids_new:
            if self._do_write(fout_txt, force):
                with open(fout_txt, mode) as prt:
                    self.prt_papers(pmid2ntpaper, prt)
                print('  {WR}: {TXT}'.format(
                    WR=self._msg_wrote(mode, pmids_all, pmids_new), TXT=fout_txt))

    @staticmethod
    def prt_keys(prt=sys.stdout):
        """Print paper keys"""
        prt.write('\nDESCRIPTION OF PAPER LINE:\n')
        prt.write('  ABC {ICITE_FMT}\n'.format(ICITE_FMT=NIHiCiteEntry.line_fmt()))
        prt.write('\n')
        prt.write('ABC:\n')
        NIHiCitePaper.prt_keys(prt)
        prt.write('\nNIH iCite details:\n')
        NIHiCiteEntry.prt_keys(prt)
        prt.write('\n')

    def prt_papers(self, pmid2ntpaper, prt=sys.stdout, prt_assc_pmids=True):
        """Print papers, including citation counts, cite_by and references list"""
        for pmid, paper in pmid2ntpaper.items():
            self.prt_paper(paper, pmid, pmid, prt, prt_assc_pmids)

    # pylint: disable=too-many-arguments
    def prt_paper(self, paper, pmid, name, prt=sys.stdout, prt_assc_pmids=True):
        """Print one paper, including citation counts, cite_by and references list"""
        if paper is not None:
            if prt_assc_pmids:
                paper.prt_summary(prt, self.rpt_references, 'cite')
                prt.write('\n')
            else:
                prt.write('TOP {iCite}\n'.format(iCite=paper.str_line()))
        else:
            prt.write('No iCite results found: {PMID} {NAME}\n\n'.format(
                PMID=pmid, NAME=name if name is not None else ''))

    @staticmethod
    def _msg_wrote(mode, pmids_req, pmids_new):
        """Get the 'WROTE' or 'APPENDED' message"""
        if mode == 'w':
            return '{N} WROTE'.format(N=len(pmids_req))
        if mode == 'a':
            if pmids_new:
                return '{N} of {M} APPENDED'.format(
                    N=len(pmids_new),
                    M=len(pmids_req))
            return '{N} of {M} FOUND'.format(
                N=len(pmids_new),
                M=len(pmids_req))
        raise RuntimeError('UNRECOGNIZED WRITE MODE({M})'.format(M=mode))

    def _get_new_pmids(self, pmidcite_txt, pmids):
        """Get PMIDs which are not already fully analyzed in pmidcite.txt"""
        if not os.path.exists(pmidcite_txt):
            return pmids
        pmids_old = self._get_old_pmids(pmidcite_txt)
        return [p for p in pmids if p not in pmids_old]

    @staticmethod
    def _get_old_pmids(pmidcite_txt):
        """Get PMIDs already found in pmidcite.txt"""
        pmids = set()
        with open(pmidcite_txt) as ifstrm:
            for line in ifstrm:
                if line[:4] == 'TOP ':
                    flds = line.split()
                    assert flds[1].isdigit(), '{} {}'.format(pmidcite_txt, flds)
                    pmids.add(int(flds[1]))
        return pmids

    def wr_name2pmid(self, fout_txt, name2pmid):
        """Run iCite for user-provided PMIDs and write to a file"""
        name2ntpaper = self._run_icite_name2pmid(name2pmid, dnld_assc_pmids=False, pmid2note=None)
        if name2ntpaper:
            with open(fout_txt, 'w') as prt:
                for name, ntpaper in name2ntpaper.items():
                    self.prt_paper(ntpaper.paper, ntpaper.pmid, name, prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def _run_icite_name2pmid(self, name2pmid, dnld_assc_pmids, pmid2note):
        """Get a NIHiCitePaper object for each user-specified PMID"""
        name2ntpaper = {}
        ntobj = cx.namedtuple('Paper', 'pmid paper')
        for name, pmid in name2pmid.items():
            ## print('NNNNNNNNNNNNNNNNNNNN', name, pmid)
            paper = self._get_paper(pmid, name, dnld_assc_pmids, pmid2note)
            name2ntpaper[name] = ntobj(pmid=pmid, paper=paper)
        return name2ntpaper

    def get_pmid2paper(self, pmids, dnld_assc_pmids, pmid2note):
        """Get a NIHiCitePaper object for each user-specified PMID"""
        s_get_paper = self._get_paper
        if not pmid2note:
            pmid_paper = [(p, s_get_paper(p, '', dnld_assc_pmids, None)) for p in pmids]
        else:
            s_p2n = pmid2note.get
            pmid_paper = [(p, s_get_paper(p, '', dnld_assc_pmids, s_p2n(p, ''))) for p in pmids]
        return cx.OrderedDict(pmid_paper)  # pmid2ntpaper

    def _get_paper(self, pmid_top, header, dnld_assc_pmids, note):
        """Print summary for each user-specified PMID"""
        citeobj_top = self.dnld_icite_pmid(pmid_top)  # NIHiCiteEntry
        if citeobj_top:
            if dnld_assc_pmids:
                self.dnld_assc_pmids(citeobj_top)
            paper = NIHiCitePaper(pmid_top, self.dir_dnld, header, note)
            return paper
        print('No results found: {PMID} {HDR} {NOTE}'.format(
            PMID=pmid_top,
            HDR=header if header else '',
            NOTE=note if note else ''))
        return None

    def dnld_assc_pmids(self, icite):
        """Download PMID iCite data for PMIDs associated with icite paper"""
        pmids_assc = icite.get_assc_pmids()
        ## print('AAAAAAAAAAAAAAAA')
        if not pmids_assc:
            return []
        ## print('BBBBBBBBBBBBBBBB')
        if self.dnld_force:
            return self.api.dnld_icites(pmids_assc)
        ## print('CCCCCCCCCCCCCCCC')
        pmids_missing = self._get_pmids_missing(pmids_assc)
        ## print('{N} PMIDs assc'.format(N=len(pmids_assc)))
        ## print('{N} PMIDs missing'.format(N=len(pmids_missing)))
        if pmids_missing:
            objs_missing = self.api.dnld_icites(pmids_missing)
            pmids_load = pmids_assc.difference(pmids_missing)
            objs_dnlded = self.load_icites(pmids_load)
            ## print('{N} PMIDs loaded'.format(N=len(pmids_load)))
            return objs_missing + objs_dnlded
        return self.load_icites(pmids_assc)
        ## print('DDDDDDDDDDDDDDDD')

    def load_icites(self, pmids):
        """Load multiple NIH iCite data from Python modules"""
        if not pmids:
            return []
        icites = []
        for pmid in pmids:
            file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=pmid)
            icites.append(self.load_icite(file_pmid))
        return icites

    @staticmethod
    def load_icite(file_pmid):
        """Load NIH iCite information from Python modules"""
        if os.path.exists(file_pmid):
            spec = importlib.util.spec_from_file_location("module.name", file_pmid)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return NIHiCiteEntry(mod.ICITE)
        return None

    def _get_pmids_missing(self, pmids_all):
        """Get PMIDs that have not yet been downloaded"""
        pmids_missing = set()
        for pmid_cur in pmids_all:
            file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=pmid_cur)
            if not os.path.exists(file_pmid):
                pmids_missing.add(pmid_cur)
        return pmids_missing

    def dnld_icite_pmid(self, pmid):
        """Download NIH iCite data for requested PMIDs"""
        file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=pmid)
        if self.dnld_force or not os.path.exists(file_pmid):
            iciteobj = self.api.dnld_icite(pmid)
            if iciteobj is not None:
                return iciteobj
        return self.load_icite(file_pmid)  # NIHiCiteEntry

    @staticmethod
    def _do_write(fout_txt, force):
        """Ask for a yes-no answer from the user on STDIN"""
        if not os.path.exists(fout_txt) or force:
            return True
        prompt_user = '\nover-write {TXT} (yes/no)? '.format(TXT=fout_txt)
        return input(prompt_user).lower()[:1] == 'y'


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
