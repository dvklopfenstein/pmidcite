"""Given a PubMed ID (PMID), download a list of publications which cite and reference it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from os.path import exists
from os.path import join
import collections as cx
from collections import OrderedDict

from pmidcite.cli.utils import read_top_pmids
from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.pmid_loader import NIHiCiteLoader


class NIHiCiteDownloader:
    """Given a PubMed ID (PMID), download a list of publications which cite and reference it"""

    def __init__(self, dir_download, force_download, details_cites_refs=None, nih_grouper=None):
        self.dnld_force = force_download
        self.api = NIHiCiteAPI()
        # Default:set()  Options:{'cited_by_clin', 'cited_by', 'references'}
        self.details_cites_refs = self._init_details_cites_refs(details_cites_refs)
        self.dir_dnld = dir_download  # Recommended dir_icite_py: ./icite
        self.nihgrouper = nih_grouper if nih_grouper is not None else NihGrouper()
        self.loader = NIHiCiteLoader(self.nihgrouper, dir_download, self.details_cites_refs)
        if not exists(dir_download):
            raise RuntimeError('**FATAL: NO DIRECTORY: {DIR}'.format(DIR=dir_download))

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
                paper.prt_summary(prt, sortby_cites='nih_group', sortby_refs='nih_group')
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

    def _get_pmids_missing(self, pmids_all):
        """Get PMIDs that have not yet been downloaded"""
        pmids_missing = set()
        for pmid_cur in pmids_all:
            file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=pmid_cur))
            if not exists(file_pmid):
                pmids_missing.add(pmid_cur)
        return pmids_missing

    def get_icites(self, pmids):
        """Download NIH iCite data for requested PMIDs"""
        # Python module filenames
        s_dir_dnld = self.dir_dnld
        pmid2py = {p:join(s_dir_dnld, 'p{PMID}.py'.format(PMID=p)) for p in pmids}
        if self.dnld_force:
            pmid2nihentry = {o.pmid: o for o in self._dnld_icites(pmid2py)}
            return [pmid2nihentry.get(pmid) for pmid in pmids]
        # Separate PMIDs into those stored in Python modules and those not
        nihentries_all = []
        pmids_pyexist1 = set(pmid for pmid, py in pmid2py.items() if exists(py))
        pmids_pyexist0 = set(pmids).difference(pmids_pyexist1)
        if pmids_pyexist1:
            nihentries_loaded = self._load_icites(pmids_pyexist1, pmid2py)
            if nihentries_loaded:
                nihentries_all.extend(nihentries_loaded)
        if pmids_pyexist0:
            nihentries_all.extend(self._dnld_icites({p:pmid2py[p] for p in pmids_pyexist0}))
        # Return results sorted in the same order as input PMIDs
        pmid2nihentry = {o.pmid:o for o in nihentries_all}
        return [pmid2nihentry.get(pmid) for pmid in pmids]

    def _load_icites(self, pmids, pmid2py):
        """Load a list of NIH citation data for PMIDs"""
        nihentries_loaded = []
        s_load_icite = self.loader.load_icite
        num_exist = len(pmids)
        for idx, pmid in enumerate(pmids, 1):
            nihentries_loaded.append(s_load_icite(pmid2py[pmid]))
            if idx%1000 == 0:
                print('NIH citation data loaded: {N:,} of {M:,}'.format(N=idx, M=num_exist))
        ## nihentries_all.extend([s_load_icite(pmid2py[p]) for p in pmids_pyexist1])
        return nihentries_loaded

    def _dnld_icites(self, pmid2foutpy):
        """Download a list of NIH citation data for PMIDs"""
        nihdicts = self.api.dnld_nihdicts(pmid2foutpy.keys())
        if nihdicts:
            s_wrpy = self._wrpy
            for nih_dict in nihdicts:
                s_wrpy(pmid2foutpy[nih_dict['pmid']], nih_dict)
            s_get_group = self.nihgrouper.get_group
            return [NIHiCiteEntry(d, s_get_group(d['nih_percentile'])) for d in nihdicts]
        return []

    def get_icite(self, pmid):
        """Load or download NIH iCite data for requested PMID"""
        ## print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP get_icite', pmid, self.dir_dnld)
        file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=pmid))
        if self.dnld_force or not exists(file_pmid):
            nih_dict = self.api.dnld_nihdict(pmid)
            if nih_dict:
                self._wrpy(file_pmid, nih_dict)
                return NIHiCiteEntry(
                    nih_dict,
                    self.nihgrouper.get_group(nih_dict['nih_percentile']))
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

    def _wrpy(self, fout_py, dct, log=None):
        """Write NIH iCite to a Python module"""
        with open(fout_py, 'w') as prt:
            self.api.prt_dct(dct, prt)
            # Setting prt to sys.stdout -> WROTE: ./icite/p10802651.py
            if log:
                log.write('  WROTE: {PY}\n'.format(PY=fout_py))


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
