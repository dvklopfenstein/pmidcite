"""Given a PubMed ID (PMID), return a list of publications which cite it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import os
import collections as cx

from pmidcite.cli.utils import read_top_pmids
from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper
from pmidcite.icite.pmid_loader import NIHiCiteLoader


class NIHiCiteDownloader:
    """Manage pubs notes files"""

    def __init__(self, force_dnld, api, rpt_references=False):
        self.rpt_references = rpt_references
        self.dnld_force = force_dnld
        self.dir_dnld = api.dir_dnld  # e.g., ./icite
        self.loader = NIHiCiteLoader(self.dir_dnld)
        self.api = api                # NIHiCiteAPI

    #### def wr_papers(self, fout_txt, force_overwrite, pmid2ntpaper, mode='w', pmid2note=None):
    ####     """Run iCite for user-provided PMIDs and write to a file"""
    ####     ## print('WWWWWWWWWWWWWWWWWWWWWWWWWWW NIHiCiteDownloader wr_papers', pmid2note)
    ####     if not pmid2ntpaper:
    ####         return
    ####     pmids_all = pmid2ntpaper.keys()
    ####     pmids_new = pmids_all
    ####     if mode == 'a':
    ####         pmids_new = self._get_new_pmids(fout_txt, pmids_all)
    ####         ## print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa pmids_new', pmids_new)
    ####     if pmids_new:
    ####         ## print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPP', pmid2ntpaper, pmid2note)
    ####         if self._do_write(fout_txt, force_overwrite):
    ####             with open(fout_txt, mode) as prt:
    ####                 pmids_prt = self.prt_papers(pmid2ntpaper, prt, pmid2note=pmid2note)
    ####             print('{WR}: {TXT}'.format(
    ####                 WR=self._msg_wrote(mode, pmids_all, pmids_prt), TXT=fout_txt))

    def wr_papers(self, fout_txt, pmid2icitepaper, force_overwrite=False, mode='w'):
        """Run iCite for user-provided PMIDs and write to a file"""
        ## print('WWWWWWWWWWWWWWWWWWWWWWWWWWW NIHiCiteDownloader wr_papers')
        if not pmid2icitepaper:
            return
        pmids_all = pmid2icitepaper.keys()
        pmids_new = pmids_all
        if mode == 'a':
            pmids_new = self._get_new_pmids(fout_txt, pmids_all)
            ## print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa pmids_new', pmids_new, pmids_all)
        if pmids_new:
            ## print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPP', pmid2icitepaper)
            if self._do_write(fout_txt, force_overwrite):
                with open(fout_txt, mode) as prt:
                    self.prt_papers(pmid2icitepaper, prt)
                print('{WR}: {TXT}'.format(
                    WR=self._msg_wrote(mode, pmids_all, pmids_new), TXT=fout_txt))

    @staticmethod
    def prt_hdr(prt=sys.stdout):
        """Print column headers in one line"""
        prt.write('KEY {HDR}\n'.format(HDR=NIHiCiteEntry.hdr))

    @staticmethod
    def prt_keys(prt=sys.stdout):
        """Print paper keys"""
        prt.write('\nKEYS TO PAPER LINE:\n')
        prt.write('    TYP {ICITE_FMT}\n'.format(ICITE_FMT=NIHiCiteEntry.line_fmt()))
        prt.write('\n')
        prt.write('TYPe of relationship to the user-requested paper (TYP):\n')
        NIHiCitePaper.prt_keys(prt)
        prt.write('\nNIH iCite details:\n\n')
        NIHiCiteEntry.prt_keys(prt)
        prt.write('\n')

    #### def prt_papers(self, pmid2ntpaper, prt=sys.stdout, prt_assc_pmids=True, pmid2note=None):
    ####     """Print papers, including citation counts, cite_by and references list"""
    ####     #print('PPPPPPPPPPPPPPPPPPPPPPPPPPP NIHiCiteDownloader prt_papers')
    ####     pmids = set()
    ####     if pmid2note is None:
    ####         pmid2note = {}
    ####     for pmid, paper in pmid2ntpaper.items():
    ####         if paper is not None:
    ####             self.prt_paper(paper, pmid, pmid, prt, prt_assc_pmids)
    ####             pmids.add(pmid)
    ####         elif pmid in pmid2note:
    ####             prt.write('TOP {PMID} {NOTE}\n'.format(PMID=pmid, NOTE=pmid2note[pmid]))
    ####             pmids.add(pmid)
    ####         else:
    ####             print('**WARNING: NO iCite ENTRY FOUND FOR: {PMID}'.format(PMID=pmid))
    ####     return pmids

    def prt_papers(self, pmid2icitepaper, prt=sys.stdout, prt_assc_pmids=True):
        """Print papers, including citation counts, cite_by and references list"""
        for pmid, paper in pmid2icitepaper.items():
            if paper is not None:
                self.prt_paper(paper, pmid, pmid, prt, prt_assc_pmids)
            else:
                print('**WARNING: NO iCite ENTRY FOUND FOR: {PMID}'.format(PMID=pmid))

    # pylint: disable=too-many-arguments
    def prt_paper(self, paper, pmid, name, prt=sys.stdout, prt_assc_pmids=True):
        """Print one paper, including citation counts, cite_by and references list"""
        if paper is not None:
            if prt_assc_pmids:
                #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX paper.prt_summary')
                paper.prt_summary(prt, self.rpt_references, sortby_cites='nih_sd', sortby_refs=None)
                prt.write('\n')
            else:
                prt.write('TOP {iCite}\n'.format(iCite=paper.str_line()))
        else:
            prt.write('No iCite results found: {PMID} {NAME}\n\n'.format(
                PMID=pmid, NAME=name if name is not None else ''))

    @staticmethod
    ## def _msg_wrote(mode, pmids_req, pmids_new):
    def _msg_wrote(mode, pmids_req, pmids_new):
        """Get the 'WROTE' or 'APPENDED' message"""
        if mode == 'w':
            return '{N:6,} WROTE'.format(N=len(pmids_req))
        if mode == 'a':
            if pmids_new:
                return '{N:,} of {M:,} APPENDED'.format(
                    N=len(pmids_new),
                    M=len(pmids_req))
            return '{N:,} of {M:,} FOUND'.format(
                N=len(pmids_new),
                M=len(pmids_req))
            # return '{N:,} FOUND'.format(M=len(pmids_req))
        raise RuntimeError('UNRECOGNIZED WRITE MODE({M})'.format(M=mode))

    @staticmethod
    def _get_new_pmids(pmidcite_txt, pmids):
        """Get PMIDs which are not already fully analyzed in pmidcite.txt"""
        if not os.path.exists(pmidcite_txt):
            return pmids
        pmids_old = read_top_pmids(pmidcite_txt)
        return [p for p in pmids if p not in pmids_old]

    def wr_name2pmid(self, fout_txt, name2pmid):
        """Run iCite for user-provided PMIDs and write to a file"""
        # pylint: disable=line-too-long
        name2ntpaper = self._run_icite_name2pmid(name2pmid, dnld_assc_pmids_do=False, pmid2note=None)
        if name2ntpaper:
            with open(fout_txt, 'w') as prt:
                for name, ntpaper in name2ntpaper.items():
                    self.prt_paper(ntpaper.paper, ntpaper.pmid, name, prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def _run_icite_name2pmid(self, name2pmid, dnld_assc_pmids_do, pmid2note):
        """Get a NIHiCitePaper object for each user-specified PMID"""
        name2ntpaper = {}
        ntobj = cx.namedtuple('Paper', 'pmid paper')
        for name, pmid in name2pmid.items():
            paper = self._geticitepaper(pmid, name, dnld_assc_pmids_do, pmid2note)
            name2ntpaper[name] = ntobj(pmid=pmid, paper=paper)
        return name2ntpaper

    def get_pmid2paper(self, pmids, dnld_assc_pmids_do, pmid2note=None, prt=sys.stdout):
        """Get a NIHiCitePaper object for each user-specified PMID"""
        ## print('NNNNNNNNNNNNNNNNNN pmidcite get_pmid2paper', pmids, dnld_assc_pmids_do, pmid2note)
        s_geticitepaper = self._geticitepaper
        if not pmid2note:
            papers = [s_geticitepaper(p, '', dnld_assc_pmids_do, None, prt) for p in pmids]
        else:
            papers = [s_geticitepaper(p, '', dnld_assc_pmids_do, pmid2note, prt) for p in pmids]
        # Note: if there is no iCite entry for a PMID, paper will be None
        return cx.OrderedDict(zip(pmids, papers))  # pmid2ntpaper

    def _geticitepaper(self, pmid_top, header, dnld_assc_pmids_do, pmid2note, prt=sys.stdout):
        """Print summary for each user-specified PMID"""
        citeobj_top = self.dnld_icite_pmid(pmid_top)  # NIHiCiteEntry
        if citeobj_top:
            if dnld_assc_pmids_do:
                self._dnld_assc_pmids(citeobj_top, prt)
            return NIHiCitePaper(pmid_top, self.dir_dnld, header, pmid2note)
        note = ''
        if pmid2note and pmid_top in pmid2note:
            note = pmid2note[pmid_top]
        print('No NIH iCite results found: {PMID} {HDR} {NOTE}'.format(
            PMID=pmid_top,
            HDR=header if header else '',
            NOTE=note))
        return None  ## TBD: NIHiCitePaper(pmid_top, self.dir_dnld, header, note)

    def _dnld_assc_pmids(self, icite, prt=sys.stdout):
        """Download PMID iCite data for PMIDs associated with icite paper"""
        pmids_assc = icite.get_assc_pmids()
        ## print('AAAAAAAAAAAAAAAA pmids_assc', pmids_assc)
        if not pmids_assc:
            return []
        ## print('BBBBBBBBBBBBBBBB self.dnld_force', self.dnld_force)
        if self.dnld_force:
            return self.api.dnld_icites(pmids_assc)
        ## print('CCCCCCCCCCCCCCCC')
        pmids_missing = self._get_pmids_missing(pmids_assc)
        ## print('{N} PMIDs assc'.format(N=len(pmids_assc)))
        ## print('{N} PMIDs missing'.format(N=len(pmids_missing)))
        if pmids_missing:
            objs_missing = self.api.dnld_icites(pmids_missing)
            pmids_load = pmids_assc.difference(pmids_missing)
            objs_dnlded = self.loader.load_icites(pmids_load, prt)
            ## print('{N} PMIDs loaded'.format(N=len(pmids_load)))
            return objs_missing + objs_dnlded
        ## print('DDDDDDDDDDDDDDDD', prt)
        return self.loader.load_icites(pmids_assc, prt)

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
        ## print('DDDDDDDDDDDDDDD dnld_icite_pmid force_dnld={F} {P} exists = {E}'.format(
        ##     F=self.dnld_force, E=os.path.exists(file_pmid), P=file_pmid))
        if self.dnld_force or not os.path.exists(file_pmid):
            ## print('DDDDDDDDDDDDDDD dnld_icite_pmid DOWNLOADING icite')
            iciteobj = self.api.dnld_icite(pmid)
            ## print('DDDDDDDDDDDDDDD dnld_icite_pmid iciteobj', iciteobj)
            if iciteobj is not None:
                return iciteobj
        return self.loader.load_icite(file_pmid)  # NIHiCiteEntry

    @staticmethod
    def _do_write(fout_txt, force_overwrite):
        """Ask for a yes-no answer from the user on STDIN"""
        if not os.path.exists(fout_txt) or force_overwrite:
            return True
        prompt_user = '\nover-write {TXT} (yes/no)? '.format(TXT=fout_txt)
        return input(prompt_user).lower()[:1] == 'y'


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
