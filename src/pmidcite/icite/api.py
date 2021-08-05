"""Given PubMed IDs (PMIDs), download NIH citation data and write it to a Python module"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import OrderedDict

import traceback
import requests

from pmidcite.icite.utils import split_list


class NIHiCiteAPI:
    """Given a PubMed ID (PMID), return a list of publications which cite it from NIH's iCite"""

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

    #           https://icite.od.nih.gov/api
    url_base = 'https://icite.od.nih.gov/api/pubs'

    flds_yes_no = {'is_research_article', 'is_clinical', 'provisional'}
    yes_no = {'Yes':True, 'No':False}

    #### def __init__(self, nihgrouper, dirpy_dnld='.', prt=None, **kws):
    def __init__(self, prt=None, **kws):
        #### self.nihgrouper = nihgrouper
        #### self.dir_dnld = dirpy_dnld
        #### if not exists(dirpy_dnld):
        ####     raise RuntimeError('**FATAL: NO DIRECTORY: {DIR}'.format(DIR=dirpy_dnld))
        self.prt = prt  # Setting prt to sys.stdout -> WROTE: ./icite/p10802651.py
        self.kws = {k:v for k, v in kws.items() if k in self.opt_keys}

    def dnld_icites(self, pmid2foutpy):
        """Run iCite on given PubMed IDs"""
        if not pmid2foutpy:
            return {}
            #### return []
        #### icites_all = []
        pmid2json = {}
        for pmid2foutpy_cur in split_list(pmid2foutpy.items(), 900):
            print('src/pmidcite/icite/api.py AAAAAAAAAAAAA', len(pmid2foutpy), len(pmid2foutpy_cur))
            #### icites_cur = self._dnld_icites(pmid2foutpy_cur)
            self._dnld_jsons(pmid2json, pmid2foutpy)
            #### if icites_cur:
            ####     icites_all.extend(icites_cur)
        return pmid2json
        #### return icites_all

    #### def _dnld_icites(self, pmid2foutpy):
    ####     """Download NIH citation data: 1 json per pmid"""
    ####     jsons = self._dnld_jsons(pmid2foutpy)
    ####     #### s_jsonpmid_to_obj = self._jsonpmid_to_obj
    ####     #### return [s_jsonpmid_to_obj(j) for j in jsons]

    def _dnld_jsons(self, pmid2jsondct, pmid2foutpy):
        """Download NIH citation data using a request using their API"""
        req_nihocc = '{URL}?pmids={PMIDS}'.format(
            URL=self.url_base,
            PMIDS=','.join(str(p) for p in pmid2foutpy))
        rsp_json = self._send_request(req_nihocc)
        if rsp_json is not None:
            s_adjust_jsondct = self._adjust_jsondct
            s_wrpy = self._wrpy
            #### adj_json_dcts = [s_adjust_jsondct(json_dct) for json_dct in rsp_json['data']]
            for nih_json_dct in rsp_json['data']:
                adj_json_dct = s_adjust_jsondct(nih_json_dct)
                pmid = adj_json_dct['pmid']
                pmid2jsondct[pmid] = adj_json_dct
                fout_py = pmid2foutpy[pmid]
                if fout_py is not None:
                    s_wrpy(fout_py, adj_json_dct)
            #### jsons = [s_adjust_jsondct(j) for j in rsp_json['data']]
            #### print(next(iter(jsons)))
            #### return jsons
        #### lst = []
        #### if rsp_json is not None:
        ####     for json_dct in rsp_json['data']:
        ####         lst.append(self._jsonpmid_to_obj(json_dct))
        #### return lst

    def dnld_icite(self, pmid, fout_pmid):
        """Download NIH citation data for one researcher-spedified PMID. Return a corrected json"""
        cmd = '/'.join([self.url_base, str(pmid)])
        adj_json_dct = self._adjust_jsondct(self._send_request(cmd))
        if fout_pmid is not None:
            self._wrpy(fout_pmid, adj_json_dct)
        return adj_json_dct if adj_json_dct else None

    def _send_request(self, cmd):
        """Send the request to iCite"""
        try:
            rsp = requests.get(cmd)
            if rsp.status_code == 200:
                return rsp.json()
            print(self._err_msg(rsp))
            return None
        except requests.exceptions.ConnectionError as errobj:
            print('**ERROR: ConnectionError = {ERR}\n'.format(ERR=str(errobj)))
            return None
        except:
            traceback.print_exc()
            raise RuntimeError('**ERROR DOWNLOADING {CMD}'.format(CMD=cmd))

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

    #### def _jsonpmid_to_obj(self, adj_json_dct):
    ####     """Given a PMID json dict, return a NIHiCiteEntry object"""
    ####     ## adj_json_dct = self._adjust_jsondct(json_dct)
    ####     file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=adj_json_dct['pmid']))
    ####     self._wrpy(file_pmid, adj_json_dct)
    ####     return NIHiCiteEntry(
    ####        adj_json_dct,
    ####        self.nihgrouper.get_group(adj_json_dct['nih_percentile']))

    def _adjust_jsondct(self, json_dct):
        """Adjust values in the json dict"""
        dct = {}
        if json_dct['title'] is not None:
            title = json_dct['title'].strip()
            if '"' in title:
                title = title.replace('"', "'")
            if "\n" in title:
                title = title.replace('\n', " ")
            dct['title'] = title
        if json_dct['authors'] is not None:
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
        return OrderedDict(lst)

    def _wrpy(self, fout_py, dct):
        """Write NIH iCite to a Python module"""
        with open(fout_py, 'w') as prt:
            self._prt_dct(dct, prt)
            if self.prt:
                self.prt.write('  WROTE: {PY}\n'.format(PY=fout_py))

    @staticmethod
    def _prt_dct(dct, prt):
        """Print NIH iCite data as a dict"""
        prt.write('"""Write data downloaded for NIH iCite data"""\n\n')
        prt.write('# pylint: disable=line-too-long\n')
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
