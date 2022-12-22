"""Summarize NIH citation data for requested papers from the commandline or in files"""

from collections import namedtuple
from collections import defaultdict

__copyright__ = "Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"


class SummarizePapers:
    """Summarize NIH citation data for requested papers from the commandline or in files"""

    def __init__(self, name, nih_grouper=None):
        self.name = name
        self.nts = None
        self.num_papers_all = None
        self.nihgrpr = nih_grouper

    def str_oneline(self):
        """Get str that is a one-line summary of many papers/citiations"""
        grp2nts = self._get_stats_grpr() if self.nihgrpr else self._get_stats_nogrpr()
        years = self.get_years()
        year_min = min(years)
        year_max = max(years)
        return '{NIHP} {Ys:3} years:{Y0:4}-{Y1:4} {N:5} papers {NAME}'.format(
            NIHP=self._str_group_percs(grp2nts),
            Ys=year_max-year_min,
            Y0=year_min,
            Y1=year_max,
            N=self.num_papers_all,
            NAME=self.name)

    def get_years(self):
        """Get the years of all publications"""
        return list(nt.year for nt in self.nts)

    def _str_group_percs(self, grp2nts):
        """Get precentages of papers in each group"""
        lst = []
        for grp in ['i', '4', '3', '2', '1', '0']:
            num_papers_grp = len(grp2nts[grp]) if grp2nts else 0
            abc = '{G}={P}'.format(
                G=grp,
                P='{:05.1f}%'.format(
                    num_papers_grp/self.num_papers_all*100) if num_papers_grp != 0 else "......")
            lst.append(abc)
        return ' '.join(lst)

    def _get_stats_grpr(self):
        """Get summary information for list of papers"""
        grp2nts = defaultdict(list)
        grpr = self.nihgrpr
        for ntd in self.nts:
            grp2nts[grpr.str_group(ntd.nih_perc)].append(ntd)
            ##print('DDDDDDDD', ntd)
        return grp2nts

    def _get_stats_nogrpr(self):
        """Get summary information for list of papers"""
        grp2nts = defaultdict(list)
        for ntd in self.nts:
            grp2nts[ntd.nih_group].append(ntd)
        return grp2nts

    @staticmethod
    def read_lines(filename, top_cit_ref):
        """Read paper citation lines"""
        if top_cit_ref is None:
            top_cit_ref = {'TOP',}  # TOP, CIT, CLI, REF
        nts = []
        nto = namedtuple('iciteline', (
            'line pmid aart nih_perc nih_group year num_cite_all num_cite num_clin num_refs'))
        with open(filename) as ifstrm:
            for line in ifstrm:
                if line[:3] in top_cit_ref:
                    flds = line.split(maxsplit=10)
                    if flds[1].isdigit():
                        num_cite = int(flds[7])
                        num_clin = int(flds[8])
                        nts.append(nto(
                            line=line.rstrip(),
                            pmid=int(flds[1]),
                            aart=f'{flds[2]} {flds[3]}',
                            nih_perc=int(flds[4]),
                            nih_group=flds[5],     # -i or a number
                            year=int(flds[6]),
                            num_cite_all=num_cite + num_clin,
                            num_cite=num_cite,
                            num_clin=num_clin,
                            num_refs=int(flds[9])))
        return nts

    # -- Constructors ------------------------------------------------------------
    @classmethod
    def from_file(cls, filename, nih_grouper=None, top_cit_ref=None):
        """Get SummarizePapers instance, given a file filled with icite lines w/TOP|CIT|CLI|REF"""
        obj = cls(filename, nih_grouper)
        obj.nts = obj.read_lines(filename, top_cit_ref)
        obj.num_papers_all = len(obj.nts)
        return obj


# Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved.
