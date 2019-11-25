"""Given a PubMed ID (PMID), return a list of publications which cite it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
#### import os
import collections as cx
#### import importlib.util
import requests

from pmidcite.icite.icite import NIHiCite
#### from pmidcite.icite.paper import NIHiCitePaper


class NIHiCiteAPI:
    """Manage pubs notes files"""

    opt_keys = {
        # Number of publications to return. The maximum allowed is 1000.
        'limit'
        # Only return publications with a PMID greater than this
        # Example: /api/pubs?offset=23456789&limit=10&format=csv
        'offset'
        # Only return publications from the given year.
        'year'
        # Only return publications with the given PubMed IDs.
        # Separate multiple IDs with commas to request up to 1000 at a time.
        # If this parameter is provided, all other parameters are ignored.
        'pmids'
        # only return publications with the given fields.
        # Separate multiple fields with commas (no space).
        # Field names are very specific and listed in Response example below.
        # No fl param will return all fields.
        # Example: /api/pubs?pmids=28968381,28324054,23843509&fl=pmid,year,title,apt
        'fl'
        # return csv (comma separated value) by specifying format=csv rather than the default JSON.
        'format'}

    url_base = 'https://icite.od.nih.gov/api/pubs'

    flds_yes_no = {'is_research_article', 'is_clinical', 'provisional'}
    yes_no = {'Yes':True, 'No':False}

    def __init__(self, dirpy_dnld='.', **kws):
        self.dir_dnld = dirpy_dnld
        self.kws = {k:v for k, v in kws.items() if k in self.opt_keys}

    def dnld_icites(self, pmids):
        """Run iCite on given PubMed IDs"""
        if not pmids:
            return []
        assert len(pmids) <= 1000, '{N} pmids > 1000'.format(N=len(pmids))
        cmd = '{URL}?pmids={PMIDS}'.format(URL=self.url_base, PMIDS=','.join(str(p) for p in pmids))
        rsp = requests.get(cmd)
        if rsp.status_code == 200:
            # Keys:
            #   'meta': {'limit': 1000, 'offset': 0, 'fl': None}
            #   'links': {
            #       'self': 'https://icite.od.nih.gov/api/pubs?limit=1000&offset=0&fl=',
            #       'next': 'https://icite.od.nih.gov/api/pubs?limit=1000&offset=1000&fl='}
            #   'data': [{'pmid': 1, 'year': 1975, ...
            lst = []
            rsp_json = rsp.json()
            for json_dct in rsp_json['data']:
                lst.append(self._jsonpmid_to_obj(json_dct))  # NIHiCite
            return lst
        raise RuntimeError(self._err_msg(rsp))

    def dnld_icite(self, pmid):
        """Run iCite on given PubMed IDs"""
        rsp = requests.get('/'.join([self.url_base, str(pmid)]))
        if rsp.status_code == 200:
            json_dct = rsp.json()
            if json_dct is not None:
                return self._jsonpmid_to_obj(json_dct)
            return None
        raise RuntimeError(self._err_msg(rsp))

    @staticmethod
    def _err_msg(rsp):
        """Get error message if an NIH iCite request failed"""
        #print('RRRRRRRRRRRRRRRRRRRRRR', dir(rsp))
        #print('RRRRRRRRRRRRRRRRRRRRRR', rsp.content)
        #print('RRRRRRRRRRRRRRRRRRRRRR', rsp.json())
        return '{CODE} {REASON}: {TEXT}'.format(
            CODE=rsp.status_code,
            REASON=rsp.reason,
            TEXT=' '.join('{K}({V})'.format(K=k, V=v) for k, v in sorted(rsp.json().items())))
            #TEXT=rsp.text)

    def _jsonpmid_to_obj(self, json_dct):
        """Given a PMID json dict, return a NIHiCite object"""
        file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=json_dct['pmid'])
        adj_dct = self._adjust_jsondct(json_dct)
        self.wrpy(file_pmid, adj_dct)
        return NIHiCite(adj_dct)

    def _adjust_jsondct(self, json_dct):
        """Adjust values in the json dict"""
        dct = {}
        if 'authors' is not None:
            dct['authors'] = json_dct['authors'].split(', ')
        yes_no = self.yes_no
        dct['is_research_article'] = yes_no[json_dct['is_research_article']]
        dct['is_clinical'] = yes_no[json_dct['is_clinical']]
        dct['provisional'] = yes_no[json_dct['provisional']]
        lst = []
        lists = {'authors', 'cited_by_clin', 'cited_by', 'references'}
        for key, val in json_dct.items():
            if key in dct:
                lst.append((key, dct[key]))
            elif key in lists:
                lst.append((key, [] if val is None else val))
            else:
                lst.append((key, val))
        return cx.OrderedDict(lst)

    def wrpy(self, fout_py, dct):
        """Write NIH iCite to a Python module"""
        with open(fout_py, 'w') as prt:
            self.prt_dct(dct, prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    @staticmethod
    def prt_dct(dct, prt=sys.stdout):
        """Print NIH iCite data as a dict"""
        iciteobj = NIHiCite(dct)
        prt.write('"""Write data downloaded for NIH iCite data"""\n\n')
        prt.write('# pylint: disable=line-too-long\n')
        prt.write('# DESC: {DESC}\n'.format(DESC=str(iciteobj)))
        prt.write('ICITE = {\n')
        str_val = {'title', 'journal', 'doi'}
        for key, val in dct.items():
            if key == 'authors':
                prt.write("    '{K}': {V},\n".format(K=key, V=val))
                #prt.write("    '{K}': {AUTHORS},\n".format(
                #    K=key,
                #    AUTHORS='\n'.join(['"{AU}"'.format(AU=a) for a in val])))
            elif key not in str_val:
                prt.write("    '{K}': {V},\n".format(K=key, V=val))
            else:
                prt.write('''    '{K}': """{V}""",\n'''.format(K=key, V=val))
        prt.write('}\n')


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
