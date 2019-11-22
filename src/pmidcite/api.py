"""Given a PubMed ID (PMID), return a list of publications which cite it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import os
import collections as cx
import importlib.util
import requests

from pmidcite.icite import NIHiCite


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

    def __init__(self, force_dnld, dir_dnld='.', mod_dir='', prt=sys.stdout, **kws):
        self.dnld_force = force_dnld
        self.dnld_dir = dir_dnld
        self.mod_dir = mod_dir
        self.prt = prt
        self.kws = {k:v for k, v in kws.items() if k in self.opt_keys}

    def run_icite(self, pmids):
        """Load or download NIH iCite data for requested PMIDs"""
        if isinstance(pmids, int):
            icite = self.dnld_icite_pmid(pmids)
            return self.dnld_assc_pmids(icite)
        raise RuntimeError('TBD IMPLEMENT')

    def dnld_assc_pmids(self, icite):
        """Download PMID iCite data for PMIDs associated with icite paper"""
        pmids_assc = self._get_accs_pmids(icite)
        ## print('AAAAAAAAAAAAAAAA')
        if not pmids_assc:
            return []
        ## print('BBBBBBBBBBBBBBBB')
        if self.dnld_force:
            return self.dnld_icites(pmids_assc)
        ## print('CCCCCCCCCCCCCCCC')
        pmids_missing = self._get_pmids_missing(pmids_assc)
        ## print('{N} PMIDs assc'.format(N=len(pmids_assc)))
        ## print('{N} PMIDs missing'.format(N=len(pmids_missing)))
        if pmids_missing:
            objs_missing = self.dnld_icites(pmids_missing)
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
            file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dnld_dir, PMID=pmid)
            icites.append(self.load_icite(file_pmid))
        return icites

    @staticmethod
    def load_icite(file_pmid):
        """Load NIH iCite information from Python modules"""
        spec = importlib.util.spec_from_file_location("module.name", file_pmid)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return NIHiCite(mod.ICITE)

    def _get_pmids_missing(self, pmids_all):
        """Get PMIDs that have not yet been downloaded"""
        pmids_missing = set()
        for pmid_cur in pmids_all:
            file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dnld_dir, PMID=pmid_cur)
            if not os.path.exists(file_pmid):
                pmids_missing.add(pmid_cur)
        return pmids_missing

    @staticmethod
    def _get_accs_pmids(icite):
        """Get PMIDs associated with the given NIH iCite data"""
        pmids = set()
        if icite.dct['cited_by_clin']:
            pmids.update(icite.dct['cited_by_clin'])
        if icite.dct['cited_by']:
            pmids.update(icite.dct['cited_by'])
        if icite.dct['references']:
            pmids.update(icite.dct['references'])
        return pmids

    def dnld_icite_pmid(self, pmid):
        """Download NIH iCite data for requested PMIDs"""
        file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dnld_dir, PMID=pmid)
        if self.dnld_force or not os.path.exists(file_pmid):
            json_dct = self.dnld_icite(pmid)
            if json_dct is not None:
                return self._jsonpmid_to_obj(file_pmid, json_dct)
        return self.load_icite(file_pmid)

    def _jsonpmid_to_obj(self, file_pmid, json_dct):
        """Given a PMID json dict, return a NIHiCite object"""
        dct = self.adjust_jsondct(json_dct)
        #self.prt_dct(dct, self.prt)
        self.wrpy(file_pmid, dct)
        return NIHiCite(json_dct)

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
                #print(json_dct.keys())
                file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dnld_dir, PMID=json_dct['pmid'])
                lst.append(self._jsonpmid_to_obj(file_pmid, json_dct))  # NIHiCite
            return lst
        raise RuntimeError(self._err_msg(rsp))

    def dnld_icite(self, pmid):
        """Run iCite on given PubMed IDs"""
        rsp = requests.get('/'.join([self.url_base, str(pmid)]))
        if rsp.status_code == 200:
            dct = rsp.json()
            return dct
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

    def adjust_jsondct(self, json_dct):
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
