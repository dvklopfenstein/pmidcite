"""Given a PubMed ID (PMID), download a list of publications which cite and reference it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from os.path import exists

from collections import namedtuple
from collections import OrderedDict

from pmidcite.cli.utils import read_top_pmids
from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.paper import NIHiCitePaper


class NIHiCiteDownloaderBase:
    """Given a PubMed ID (PMID), download a list of publications which cite and reference it"""

    def __init__(self, details_cites_refs=None, nih_grouper=None):
        self.api = NIHiCiteAPI()
        # Default:set()  Options:{'cited_by_clin', 'cited_by', 'references'}
        self.details_cites_refs = self._init_details_cites_refs(details_cites_refs)
        self.nihgrouper = nih_grouper if nih_grouper is not None else NihGrouper()

    def get_icites(self, pmids):
        """Citation data should be downloaded or loaded by derived classes"""
        # pylint: disable=unreachable,no-self-use,useless-return
        raise RuntimeError("**FATAL NIHiCiteDownloaderBase:get_icites(pmids)")
        return []

    def get_icite(self, pmid):
        """Citation data should be downloaded or loaded by derived classes"""
        # pylint: disable=unreachable,no-self-use
        raise RuntimeError("**FATAL NIHiCiteDownloaderBase:get_icite(pmid)")
        return False

    def wr_papers(self, fout_txt, pmid2icitepaper, force_overwrite=False, mode='w'):
        """Run iCite for user-provided PMIDs and write to a file"""
        if not pmid2icitepaper:
            return
        pmids_all = pmid2icitepaper.keys()
        pmids_new = pmids_all
        if mode == 'a':
            pmids_new = self._get_new_pmids(fout_txt, pmids_all)
        if pmids_new:
            if self._do_write(fout_txt, force_overwrite):
                ## print('STARTING ', mode)
                with open(fout_txt, mode) as prt:
                    self.prt_papers(pmid2icitepaper, prt)
                print('{WR}: {TXT}'.format(
                    WR=self._msg_wrote(mode, pmids_all, pmids_new), TXT=fout_txt))

    @staticmethod
    def prt_hdr(prt=stdout):
        """Print column headers in one line"""
        prt.write('TYP {HDR}\n'.format(HDR=NIHiCiteEntry.hdr))

    @staticmethod
    def prt_keys(prt=stdout):
        """Print paper keys"""
        prt.write('\nKEYS TO PAPER LINE:\n')
        prt.write('    TYP {ICITE_FMT}\n'.format(ICITE_FMT=NIHiCiteEntry.line_fmt()))
        prt.write('\n')
        prt.write('TYPe of relationship to the user-requested paper (TYP):\n')
        NIHiCitePaper.prt_keys(prt)
        prt.write('\nNIH iCite details:\n\n')
        NIHiCiteEntry.prt_key_desc(prt)
        prt.write('\n')

    @staticmethod
    def prt_top(paper, prt=stdout):
        """Print one detailed line summarizing the paper"""
        prt.write('TOP {iCite}\n'.format(iCite=paper.str_line()))

    def prt_papers(self, pmid2icitepaper, prt=stdout):
        """Print papers, including citation counts, cite_by and references list"""
        for pmid, paper in pmid2icitepaper.items():
            if paper is not None:
                self.prt_paper(paper, pmid, pmid, prt)
            else:
                print('**WARNING: NO iCite ENTRY FOUND FOR: {PMID}'.format(PMID=pmid))

    def prt_paper(self, paper, pmid, name, prt=stdout):
        """Print one paper, including citation counts, cite_by and references list"""
        if paper is not None:
            if self.details_cites_refs:
                paper.prt_summary(prt, sortby_cites='nih_group', sortby_refs='nih_group')
                prt.write('\n')
            else:
                self.prt_top(paper, prt)
        else:
            prt.write('No iCite results found: {PMID} {NAME}\n\n'.format(
                PMID=pmid, NAME=name if name is not None else ''))

    @staticmethod
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
        if not exists(pmidcite_txt):
            return pmids
        pmids_old = read_top_pmids(pmidcite_txt)
        return [p for p in pmids if p not in pmids_old]

    def wr_name2pmid(self, fout_txt, name2pmid):
        """Run iCite for user-provided PMIDs and write to a file"""
        name2ntpaper = self._run_icite_name2pmid(name2pmid, pmid2note=None)
        if name2ntpaper:
            with open(fout_txt, 'w') as prt:
                for name, ntpaper in name2ntpaper.items():
                    self.prt_paper(ntpaper.paper, ntpaper.pmid, name, prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def _run_icite_name2pmid(self, name2pmid, pmid2note):
        """Get a NIHiCitePaper object for each user-specified PMID"""
        name2ntpaper = {}
        ntobj = namedtuple('Paper', 'pmid paper')
        for name, pmid in name2pmid.items():
            paper = self._geticitepaper(pmid, name, pmid2note)
            name2ntpaper[name] = ntobj(pmid=pmid, paper=paper)
        return name2ntpaper

    def get_pmid2paper(self, pmids_top, pmid2note=None):
        """Get one NIHiCitePaper object for each user-specified PMID"""
        s_geticitepaper = self._geticitepaper
        header = ''
        if not self.details_cites_refs:
            pmid_paper = []
            pmid2icite = {o.pmid:o for o in self.get_icites(pmids_top)}
            for pmid in pmids_top:
                if pmid in pmid2icite:
                    nihicite = pmid2icite[pmid]
                    paper = NIHiCitePaper(pmid, {pmid:nihicite}, '', pmid2note)
                    pmid_paper.append((pmid, paper))
            return OrderedDict(pmid_paper)
        if not pmid2note:
            papers = [s_geticitepaper(p, header, None) for p in pmids_top]
        else:
            papers = [s_geticitepaper(p, header, pmid2note) for p in pmids_top]
        # Note: if there is no iCite entry for a PMID, paper will be None
        return OrderedDict(zip(pmids_top, papers))  # pmid2ntpaper

    def get_paper(self, pmid, pmid2note=None):
        """Get one NIHiCitePaper object for each user-specified PMID"""
        return self._geticitepaper(pmid, header='', pmid2note=None if not pmid2note else pmid2note)

    def _geticitepaper(self, pmid_top, header, pmid2note):
        """Print summary for each user-specified PMID"""
        # pylint: disable=no-member
        top_nih_icite_entry = self.get_icite(pmid_top)  # get NIHiCiteEntry
        if top_nih_icite_entry:
            pmid2icite = {top_nih_icite_entry.pmid:top_nih_icite_entry}
            if self.details_cites_refs:
                assoc_pmids = top_nih_icite_entry.get_assc_pmids(self.details_cites_refs)
                for nihentry in self.get_icites(assoc_pmids):
                    pmid2icite[nihentry.pmid] = nihentry
            return NIHiCitePaper(pmid_top, pmid2icite, header, pmid2note)
        note = ''
        if pmid2note and pmid_top in pmid2note:
            note = pmid2note[pmid_top]
        print('No NIH iCite results found: {PMID} {HDR} {NOTE}'.format(
            PMID=pmid_top,
            HDR=header if header else '',
            NOTE=note))
        return None  ## TBD: NIHiCitePaper(pmid_top, self.dir_dnld, header, note)

    @staticmethod
    def _do_write(fout_txt, force_overwrite):
        """Ask for a yes-no answer from the user on STDIN"""
        if not exists(fout_txt) or force_overwrite:
            return True
        prompt_user = '\nover-write {TXT} (yes/no)? '.format(TXT=fout_txt)
        return input(prompt_user).lower()[:1] == 'y'

    @staticmethod
    def _init_details_cites_refs(details_cites_refs):
        """Initialize associated PMID keys"""
        # Default: Only load requested PMID (not citations or references)
        if details_cites_refs is None:
            return set()
        if details_cites_refs == 'all':
            return NIHiCiteEntry.associated_pmid_keys
        if details_cites_refs == 'citations':
            return NIHiCiteEntry.citekeys
        if details_cites_refs == 'references':
            return NIHiCiteEntry.refkey
        if isinstance(details_cites_refs, str):
            msg = ('**FATAL VALUE({V}) IN NIHiCiteDownloader(details_cites_refs="{V}"): '
                   'EXPECTED ONE OF: all citations references')
            raise RuntimeError(msg.format(V=details_cites_refs))
        return set(details_cites_refs).intersection(NIHiCiteEntry.associated_pmid_keys)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
