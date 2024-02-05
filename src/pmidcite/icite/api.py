"""Given PubMed IDs (PMIDs), download NIH citation data and write it to a Python module"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

## from timeit import default_timer
from collections import OrderedDict

import traceback
import requests

from pmidcite.icite.utils import split_list
## from tests.prt_hms import prt_hms


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

    def __init__(self, **kws):
        self.kws = {k:v for k, v in kws.items() if k in self.opt_keys}
        self.msgs = []

    def dnld_nihdict(self, pmid):
        """Download NIH citation data for one researcher-spedified PMID. Return a corrected json"""
        rsp_json = self._send_request(f'{self.url_base}/{pmid}')
        return self._adjust_jsondct(rsp_json) if rsp_json else None

    def dnld_nihdicts(self, pmids):
        """Download a list of NIH citation data for given PMIDs"""
        return self._dnld_gtmax(pmids) if len(pmids) > 1000 else self._dnld_ltmax(pmids)

    def _dnld_gtmax(self, pmids):
        """Run iCite on given PubMed IDs"""
        nih_dicts_all = []
        max_limit = 1000
        pmid_list_all = pmids if isinstance(pmids, list) else list(pmids)
        num_total = len(pmids)
        # The NIH-OCC allows for a maximum of 1,000 PMIDs to be downloaded at once
        for pmid_list_cur in split_list(pmid_list_all, max_limit):
            nih_dicts_cur = self._dnld_ltmax(pmid_list_cur)
            if nih_dicts_cur:
                nih_dicts_all.extend(nih_dicts_cur)
            # pylint: disable=line-too-long
            print(f'NIH citation data downloaded: {len(nih_dicts_all):,} of {num_total:,}')
        return nih_dicts_all

    def _dnld_ltmax(self, pmids):
        """Download NIH citation data using a request using their API"""
        ## tic = default_timer()
        pmids_str = ','.join(str(p) for p in pmids)
        req_nihocc = f'{self.url_base}?pmids={pmids_str}'
        ## tic = prt_hms(tic, "Create request")
        # Note: rsp_json['data'] returned from NIH not in same order as requested
        rsp_json = self._send_request(req_nihocc)
        ## tic = prt_hms(tic, "Send request. Get response")
        if rsp_json is not None:
            # Adjust the jsons downloaded for NIH citation data
            nih_dicts = []
            s_adjust_jsondct = self._adjust_jsondct
            pmids_downloaded = set()
            for nih_json_dct in rsp_json['data']:
                pmids_downloaded.add(nih_json_dct['pmid'])
                nih_dicts.append(s_adjust_jsondct(nih_json_dct))
            ## tic = prt_hms(tic, "Adjust reponse")
            # Report PMIDs that did not have NIH citation data downloaded
            pmids_missing = set(pmids).difference(pmids_downloaded)
            # pylint: disable=line-too-long
            if pmids_missing:
                print(f"**WARNING: {len(pmids_str):,} NIH CITATION DATA NOT DOWNLOADED FOR PMIDs: {pmids_str}")
            return nih_dicts
        # pylint: disable=line-too-long
        print(f"**WARNING: {len(pmids_str):,} NIH CITATION DATA NOT DOWNLOADED FOR PMIDs: {pmids_str}")
        return None


    def _send_request(self, cmd, timeout=500):
        """Send the request to iCite"""
        try:
            rsp = requests.get(cmd, timeout=timeout)
            if rsp.status_code == 200:
                return rsp.json()
            self._prt_errmsg(self._err_msg(rsp))
            return None
        except requests.exceptions.ConnectionError as errobj:
            self._prt_errmsg(f'**ERROR: ConnectionError = {str(errobj)}\n')
            return None
        # TODO: Consider explicitly re-raising using
        # 'raise RuntimeError(f'**ERROR DOWNLOADING {cmd}\n{error}') from error'
        except:
            traceback.print_exc()
            raise RuntimeError(f'**ERROR DOWNLOADING {cmd}')

    def _prt_errmsg(self, errmsg):
        """Print the error and add the error to the list of API messages"""
        print(errmsg)
        self.msgs.append(errmsg)

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
        return f'{rsp.status_code} {rsp.reason} URL[{len(rsp.url)}]: {rsp.url}'

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
            authors = json_dct['authors']
            if authors == '':
                dct['authors'] = []
            else:
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

    @staticmethod
    def prt_dct(dct, prt):
        """Print NIH iCite data as a dict"""
        prt.write('"""Write data downloaded for NIH iCite data"""\n\n')
        prt.write('# pylint: disable=line-too-long\n')
        prt.write('ICITE = {\n')
        str_val = {'title', 'journal', 'doi', 'last_modified'}
        for key, val in dct.items():
            if key == 'authors':
                prt.write(f"    '{key}': {val},\n")
                #prt.write("    '{K}': {AUTHORS},\n".format(
                #    K=key,
                #    AUTHORS='\n'.join(['"{AU}"'.format(AU=a) for a in val])))
            elif key not in str_val:
                prt.write(f"    '{key}': {val},\n")
            else:
                prt.write(f'''    '{key}': """{val}""",\n''')
        prt.write('}\n')


# Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved.
