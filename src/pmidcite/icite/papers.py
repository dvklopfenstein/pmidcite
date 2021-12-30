"""Holds NIH iCite data for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import Counter
from collections import defaultdict


class NIHiCitePapers:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    def __init__(self, pmid2paper):
        self.pmid2paper = pmid2paper
        self.author2cnt = self._init_au2cnt()
        self.au2firstlast = self._init_au2firstlast(self.author2cnt.keys())

    def get_pmid2fl(self, authors):
        """Given a list of author names, return pmid2[FfL]"""
        # {'Jo Lynne Rokita', 'Jo Lynne Harenza', 'J L Harenza'})
        pmid2firstlast = {}
        for author in authors:
            if author in self.au2firstlast:
                ## print('FFFFFFFFFFFFFFFFFFF', author, firstlast)
                for mark, pmids in self.au2firstlast[author].items():
                    for pmid in pmids:
                        pmid2firstlast[pmid] = mark
        return pmid2firstlast

    def prt_authors(self, coauthor2mark, prt_top_n=15):
        """Print authors w/most collaborations and relevant researchers"""
        for idx, (author, cnt) in enumerate(self.author2cnt.most_common()):
            seen = self._get_mark(author, coauthor2mark)
            firstlast = self.get_firstlast(author)
            if idx < prt_top_n or seen != '':
            ## if True:
                print('{S:>6} {N:3} {FL:6} {AU}'.format(FL=firstlast, S=seen, N=cnt, AU=author))
        print('{A} authors (appeared N times, M people): {LST}'.format(
            A=len(self.author2cnt),
            LST=sorted(Counter(self.author2cnt.values()).items())))

    def get_firstlast(self, author):
        """Get a string describing First and Last author affiliation"""
        if author not in self.au2firstlast:
            return ''
        firstlast = self.au2firstlast[author]
        # First author counts
        ret = 'F{N}'.format(N=len(firstlast['F'])) if 'F' in firstlast else '..'
        # Second author counts
        ret += 'f{N}'.format(N=len(firstlast['f'])) if 'f' in firstlast else '..'
        # Last author counts
        ret += 'L{N}'.format(N=len(firstlast['L'])) if 'L' in firstlast else '..'
        return ret

    def _init_au2firstlast(self, authors):
        """Get the number of times an author is in the first, middle, or last position"""
        au2firstlast = defaultdict(lambda: defaultdict(set))  # Author -to- First, Middle, Last
        for pmid, paper in self.pmid2paper.items():
            icite = paper.pmid2icite[pmid]
            authors = icite.dct['authors']
            ## print('PPPPPPPPPPPP', pmid, paper)
            if authors:
                ## print('PPPPPPPPPPPP', authors)
                # Count instances of being first or last author
                au2firstlast[authors[0]]['F'].add(pmid)
                au2firstlast[authors[-1]]['L'].add(pmid)
                if len(authors) > 2:
                    au2firstlast[authors[1]]['f'].add(pmid)
        return au2firstlast

    def _init_au2cnt(self):
        """List each co-author w/the number of times they co-author in pmid2paper"""
        authors = Counter()
        for pmid, paper in self.pmid2paper.items():
            icite = paper.pmid2icite[pmid]
            for author in icite.dct['authors']:
                authors[author] += 1
            ## print('sssssssssss', pmid, icite.dct)
        return authors

    @staticmethod
    def _get_mark(author, coauthor2mark):
        """Get a match, given a full author name"""
        for coau, mrk in coauthor2mark.items():
            if coau in author:
                return mrk
        return ''


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
