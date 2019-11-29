"""Python Wrapper for PMC's ID Converter API"""
# https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
#### import os
#### import collections as cx
import requests

from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.cfgparser.eutils import EUtilsCfg


class IdConverterAPI:
    """Python Wrapper for PMC's ID Converter API"""

    opt_keys = {
        'idtype' : {   # Example:
            "pmcid",  # PMC3531190
            "pmid",   # 23193287
            "mid",    # NIHMS311352
            "doi",    # 10.1093/nar/gks1195
        },
        'format' : {"html", "xml", "json", "csv"},
        'version' : {True: "yes", False: "no"},  # Supress versions
    }

    url_base = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
    max_ids = 200

    #### flds_yes_no = {'is_research_article', 'is_clinical', 'provisional'}
    #### yes_no = {'Yes':True, 'No':False}

    def __init__(self, dirpy_dnld='.'):
        # EUtilsCfg reads the email, apikey, and tool from file, .eutilsrc needed for the E-utils API
        # To prevent your API key from being public,
        # don't store .eutilsrc in a public repo.
        # export PMIDCITECONF=.eutilsrc
        _cfg = EUtilsCfg()
        self.email = _cfg.get_email()
        self.tool = _cfg.get_tool()
        self.dir_dnld = dirpy_dnld

    def dnld_ids(self, ids, **params):
        """Run iCite on given PubMed IDs"""
        if not ids:
            return []
        ids = list(ids)
        num_ids = len(ids)
        # TBD: https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n#1625023
        cmd = self._get_cmd(ids, **params)
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
            # for json_dct in rsp_json['data']:
            #     lst.append(self._jsonpmid_to_obj(json_dct))  # NIHiCiteEntry
            # return lst
        raise RuntimeError(self._err_msg(rsp))

    def _get_cmd(self, ids, **params):
        """Assemble the ID Converter API command"""
        cmd = '{URL}?ids={PMIDS}&email={EMAIL}&tool={TOOL}'.format(
            URL=self.url_base,
            PMIDS=','.join(str(p) for p in ids),
            EMAIL=self.email,
            TOOL=self.tool)
        if not params:
            return cmd
        option2val = self._get_option2val(**params)
        return '&'.join(['{K}={V}'.format(K=k, V=v) for k, v in option2val.items()])

    def _get_option2val(self, **params):
        """Get optional arguments for the ID Converter API command"""
        option2val = {}
        opts = self.opt_keys
        if 'idtype' in params:
            self._set_option2val(params['idtype'], 'idtype', option2val)
        if 'format' in params:
            self._set_option2val(params['format'], 'format', option2val)
        if 'version' in params:
            val = params['version']
            if val in opts['version']:
                bval = params['version']
                option2val['version'] = opts['version'][bval]
        return option2val

    def _set_option2val(self, val, key, option2val):
        """Set user-specified val in options, if it is expected"""
        if val in self.opt_keys[key]:
            option2val[key] = val
        else:
            print('**WARNING: UNKNOWN {KEY}({V})'.format(KEY=key, V=val))

    def dnld_icite(self, pmid):
        """Run iCite on given PubMed IDs"""
        rsp = requests.get('/'.join([self.url_base, str(pmid)]))
        if rsp.status_code == 200:
            json_dct = rsp.json()
            if json_dct is not None:
                return self._jsonpmid_to_obj(json_dct)
            return None
        #### raise RuntimeError(self._err_msg(rsp))
        print(self._err_msg(rsp))
        return None

    @staticmethod
    def _err_msg(rsp):
        """Get error message if an NIH iCite request failed"""
        ## print('1 RRRRRRRRRRRRRRRRRRRRRR', dir(rsp))
        ## print('2 RRRRRRRRRRRRRRRRRRRRRR', rsp.status_code)
        ## print('3 RRRRRRRRRRRRRRRRRRRRRR', rsp.reason)
        ## print('4 RRRRRRRRRRRRRRRRRRRRRR', rsp.content)
        ## print('5 RRRRRRRRRRRRRRRRRRRRRR', rsp.text)
        ## #print('3 RRRRRRRRRRRRRRRRRRRRRR', rsp.json())
        ## print('6 RRRRRRRRRRRRRRRRRRRRRR', rsp.url)
        ## if rsp.json() is not None:
        ##     txt =' '.join('{K}({V})'.format(K=k, V=v) for k, v in sorted(rsp.json().items()))
        return '{CODE} {REASON} URL[{N}]: {URL}'.format(
            CODE=rsp.status_code,
            REASON=rsp.reason,
            N=len(rsp.url),
            URL=rsp.url)
            #TEXT=rsp.text)

    def _jsonpmid_to_obj(self, json_dct):
        """Given a PMID json dict, return a NIHiCiteEntry object"""
        file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=json_dct['pmid'])
        adj_dct = self._adjust_jsondct(json_dct)
        self.wrpy(file_pmid, adj_dct)
        return NIHiCiteEntry(adj_dct)

    def _adjust_jsondct(self, json_dct):
        """Adjust values in the json dict"""
        return json_dct
        #### dct = {}
        #### if 'authors' is not None:
        ####     dct['authors'] = json_dct['authors'].split(', ')
        #### yes_no = self.yes_no
        #### dct['is_research_article'] = yes_no[json_dct['is_research_article']]
        #### dct['is_clinical'] = yes_no[json_dct['is_clinical']]
        #### dct['provisional'] = yes_no[json_dct['provisional']]
        #### lst = []
        #### lists = {'authors', 'cited_by_clin', 'cited_by', 'references'}
        #### for key, val in json_dct.items():
        ####     if key in dct:
        ####         lst.append((key, dct[key]))
        ####     elif key in lists:
        ####         lst.append((key, [] if val is None else val))
        ####     else:
        ####         lst.append((key, val))
        #### return cx.OrderedDict(lst)

    def wrpy(self, fout_py, dct):
        """Write NIH iCite to a Python module"""
        with open(fout_py, 'w') as prt:
            self.prt_dct(dct, prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    @staticmethod
    def prt_dct(dct, prt=sys.stdout):
        """Print NIH iCite data as a dict"""
        iciteobj = NIHiCiteEntry(dct)
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
