"""Given a PubMed ID (PMID), return a list of publications which cite it from NIH's iCite"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os.path import exists
from os.path import join
from sys import stdout
import collections as cx
import traceback
import requests

from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.nih_grouper import NihGrouper


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

    url_base = 'https://icite.od.nih.gov/api/pubs'

    flds_yes_no = {'is_research_article', 'is_clinical', 'provisional'}
    yes_no = {'Yes':True, 'No':False}

    def __init__(self, nihgrouper, dirpy_dnld='.', prt=None, **kws):
        self.nihgrouper = nihgrouper
        self.dir_dnld = dirpy_dnld
        if not exists(dirpy_dnld):
            raise RuntimeError('**FATAL: NO DIRECTORY: {DIR}'.format(DIR=dirpy_dnld))
        self.prt = prt
        self.kws = {k:v for k, v in kws.items() if k in self.opt_keys}

    def dnld_icites(self, pmids):
        """Run iCite on given PubMed IDs"""
        if not pmids:
            return []
        num_pmids = len(pmids)
        if num_pmids > 1000:
            print('{N} pmids > 1000'.format(N=num_pmids))
            pmids = sorted(p for p in pmids if isinstance(p, int))
            ## print(pmids)
            print('**WARNING: USING pmids[:900]')
            pmids = pmids[:900]
        ## assert len(pmids) <= 1000, '{N} pmids > 1000'.format(N=len(pmids))
        cmd = '{URL}?pmids={PMIDS}'.format(URL=self.url_base, PMIDS=','.join(str(p) for p in pmids))
        rsp_json = self._send_request(cmd)
        lst = []
        if rsp_json is not None:
            for json_dct in rsp_json['data']:
                lst.append(self._jsonpmid_to_obj(json_dct))  # NIHiCiteEntry
        return lst

    def dnld_icite(self, pmid):
        """Run iCite on given PubMed IDs"""
        cmd = '/'.join([self.url_base, str(pmid)])
        json_dct = self._send_request(cmd)
        return self._jsonpmid_to_obj(json_dct) if json_dct else None

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

    def _jsonpmid_to_obj(self, json_dct):
        """Given a PMID json dict, return a NIHiCiteEntry object"""
        file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=json_dct['pmid']))
        adj_dct = self._adjust_jsondct(json_dct)
        self._wrpy(file_pmid, adj_dct)
        return NIHiCiteEntry(adj_dct, self.nihgrouper.get_group(adj_dct['nih_percentile']))

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
        return cx.OrderedDict(lst)

    def _wrpy(self, fout_py, dct):
        """Write NIH iCite to a Python module"""
        with open(fout_py, 'w') as prt:
            self.prt_dct(dct, prt)
            if self.prt:
                self.prt.write('  WROTE: {PY}\n'.format(PY=fout_py))

    def prt_dct(self, dct, prt=stdout):
        """Print NIH iCite data as a dict"""
        iciteobj = NIHiCiteEntry(dct, self.nihgrouper.get_group(dct['nih_percentile']))
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
