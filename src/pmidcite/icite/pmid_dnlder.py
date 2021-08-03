"""Given a PubMed ID (PMID), download a list of publications which cite and reference it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from os.path import exists
from os.path import join
import collections as cx

from pmidcite.cli.utils import read_top_pmids
from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper
from pmidcite.icite.pmid_loader import NIHiCiteLoader


class NIHiCiteDownloader:
    """Given a PubMed ID (PMID), download a list of publications which cite and reference it"""

    def __init__(self, force_dnld, api, details_cites_refs=None):
        self.dnld_force = force_dnld
        self.api = api                # NIHiCiteAPI
        # Default:set()  Options:{'cited_by_clin', 'cited_by', 'references'}
        self.details_cites_refs = self._init_details_cites_refs(details_cites_refs)
        self.dir_dnld = api.dir_dnld  # e.g., ./icite
        self.nihgrouper = api.nihgrouper
        self.loader = NIHiCiteLoader(self.nihgrouper, self.dir_dnld, self.details_cites_refs)

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

    def prt_papers(self, pmid2icitepaper, prt=stdout):
        """Print papers, including citation counts, cite_by and references list"""
        for pmid, paper in pmid2icitepaper.items():
            if paper is not None:
                self.prt_paper(paper, pmid, pmid, prt)
            else:
                print('**WARNING: NO iCite ENTRY FOUND FOR: {PMID}'.format(PMID=pmid))

    # pylint: disable=too-many-arguments
    def prt_paper(self, paper, pmid, name, prt=stdout):
        """Print one paper, including citation counts, cite_by and references list"""
        if paper is not None:
            if self.details_cites_refs:
                # pylint: disable=line-too-long
                paper.prt_summary(prt, sortby_cites='nih_sd', sortby_refs='nih_sd')
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
        # pylint: disable=line-too-long
        name2ntpaper = self._run_icite_name2pmid(name2pmid, pmid2note=None)
        if name2ntpaper:
            with open(fout_txt, 'w') as prt:
                for name, ntpaper in name2ntpaper.items():
                    self.prt_paper(ntpaper.paper, ntpaper.pmid, name, prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def _run_icite_name2pmid(self, name2pmid, pmid2note):
        """Get a NIHiCitePaper object for each user-specified PMID"""
        name2ntpaper = {}
        ntobj = cx.namedtuple('Paper', 'pmid paper')
        for name, pmid in name2pmid.items():
            paper = self._geticitepaper(pmid, name, pmid2note)
            name2ntpaper[name] = ntobj(pmid=pmid, paper=paper)
        return name2ntpaper

    def get_pmid2paper(self, pmids_top, pmid2note=None):
        """Get one NIHiCitePaper object for each user-specified PMID"""
        s_geticitepaper = self._geticitepaper
        header = ''
        if not pmid2note:
            papers = [s_geticitepaper(p, header, None) for p in pmids_top]
        else:
            papers = [s_geticitepaper(p, header, pmid2note) for p in pmids_top]
        # Note: if there is no iCite entry for a PMID, paper will be None
        return cx.OrderedDict(zip(pmids_top, papers))  # pmid2ntpaper

    def _geticitepaper(self, pmid_top, header, pmid2note):
        """Print summary for each user-specified PMID"""
        top_nih_icite_entry = self.get_icite(pmid_top)  # NIHiCiteEntry
        if top_nih_icite_entry:
            if self.details_cites_refs:
                assoc_pmids = top_nih_icite_entry.get_assc_pmids(self.details_cites_refs)
                self._dnld_assc_pmids(assoc_pmids)
            # Load TOP paper. If requested, load CIT, CLI, and REF
            icites = self.loader.load_icite_mods_all([pmid_top])
            ## print('WWWWWWWWWWWWWWWW pmid_top   ', pmid_top)
            ## print('WWWWWWWWWWWWWWWW len(icites)', len(icites), [o.dct['pmid'] for o in icites])
            ## print('WWWWWWWWWWWWWWWW header     ', str(header))
            pmid2icite = {o.dct['pmid']:o for o in icites}
            return NIHiCitePaper(pmid_top, pmid2icite, header, pmid2note)
        note = ''
        if pmid2note and pmid_top in pmid2note:
            note = pmid2note[pmid_top]
        print('No NIH iCite results found: {PMID} {HDR} {NOTE}'.format(
            PMID=pmid_top,
            HDR=header if header else '',
            NOTE=note))
        return None  ## TBD: NIHiCitePaper(pmid_top, self.dir_dnld, header, note)

    def _dnld_assc_pmids(self, pmids_assc):
        """Download PMID iCite data for PMIDs associated with icite paper"""
        if not pmids_assc:
            return []
        if self.dnld_force:
            ## print('pppppppppppppppppppppp NIHiCiteDownloader _dnld_assc_pmids:', pmids_assc)
            return self.api.dnld_icites(pmids_assc)
        pmids_missing = self._get_pmids_missing(pmids_assc)
        if pmids_missing:
            objs_missing = self.api.dnld_icites(pmids_missing)
            pmids_load = pmids_assc.difference(pmids_missing)
            objs_dnlded = self.loader.load_icites(pmids_load)
            return objs_missing + objs_dnlded
        return self.loader.load_icites(pmids_assc)

    def _get_pmids_missing(self, pmids_all):
        """Get PMIDs that have not yet been downloaded"""
        pmids_missing = set()
        for pmid_cur in pmids_all:
            file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=pmid_cur))
            if not exists(file_pmid):
                pmids_missing.add(pmid_cur)
        return pmids_missing

    def get_icites(self, pmids):
        """Load or download NIH iCite data for requested PMIDs"""
        icites = []
        for pmid in pmids:
            icite = self.get_icite(pmid)
            if icite is not None:
                icites.append(icite)
        return icites

    def get_icite(self, pmid):
        """Load or download NIH iCite data for requested PMID"""
        file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=pmid))
        if self.dnld_force or not exists(file_pmid):
            iciteobj = self.api.dnld_icite(pmid)
            if iciteobj is not None:
                return iciteobj
        return self.loader.load_icite(file_pmid)  # NIHiCiteEntry

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
