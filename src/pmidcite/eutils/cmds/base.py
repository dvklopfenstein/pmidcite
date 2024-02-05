"""This script downloads NCBI records based on user search query"""

# Entrez Help: # https://www.ncbi.nlm.nih.gov/books/NBK3837/
# APIKEY: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
#
# A General Introduction to the E-utilities: # https://www.ncbi.nlm.nih.gov/books/NBK25497/
#
# Entrez-Utilities Help: # http://www.ncbi.nlm.nih.gov/books/NBK25501/
#
# The E-utilities In-Depth: Parameters, Syntax and More:
# http://www.ncbi.nlm.nih.gov/books/NBK25499/
# http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch

# tags: # https://www.ncbi.nlm.nih.gov/books/NBK3827/table/pubmedhelp.Tn/


__copyright__ = "Copyright (C) 2014-present DV Klopfenstein, PhD. All rights reserved."
__author__ = 'DV Klopfenstein, PhD'

import sys
import traceback
import json
import collections as cx
#import re
from xml.etree import ElementTree

import time

import urllib
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError as _URLError
from urllib.error import HTTPError as _HTTPError


# pylint: disable=useless-object-inheritance
class EntrezUtilities(object):
    """Helper class for Entrez E-Utilities"""

    cgifmt = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{ECMD}.fcgi"
    pat = 'PMIDs/epost={P} PMIDs/efetch={F} querykey({Q} of {Qmax}) start({S})'

    max_tries = 3
    sleep_between_tries = 15

    def __init__(self, email, apikey, tool, log=sys.stdout):
        self.email = email
        self.api_key = apikey
        self.tool = tool
        self.previous = 0
        self.log = log

    def get_database_list(self):
        """Get a list of Entrez databases"""
        # einfo: http://www.ncbi.nlm.nih.gov/books/NBK25499/
        rsp = self.run_eutilscmd('einfo', retmode='json')
        if rsp and 'einforesult' in rsp and 'dblist' in rsp['einforesult']:
            return rsp['einforesult']['dblist']
        return None

    def epost_ids(self, ids, database, num_ids_p_epost, retmax, **medline_text):
        """Post IDs using EPost"""
        epost_rsp = self.epost(database, ids, num_ids_p_epost=num_ids_p_epost)
        ## print('EPOST RSP', epost_rsp)
        # Set EFetch params
        efetch_params = dict(medline_text)
        efetch_params['webenv'] = epost_rsp['webenv']
        efetch_params['retmax'] = retmax  # num_ids_p_efetch
        # Run EFetches
        efetch_idxs = self._get_efetch_indices(epost_rsp, retmax, len(ids))
        #efetch_idxs = self._get_efetch_indices(epost_rsp, retmax, epost_rsp['count'])
        return efetch_idxs, efetch_params

    def _get_efetch_indices(self, epost_rsp, num_pmids_p_efetch, num_pmids):
        """Get EFetech list of: querykey_cur, pmids_cur, start"""
        # pmids num_pmids_p_epost num_pmids_p_efetch  ->  num_efetches
        # ----- ----------------- ------------------      ------------
        #     5                 2                  3                 3
        #     5                 2                  1                 5
        nts = []
        querykey_max = epost_rsp['querykey']
        num_pmids_p_epost_cur = epost_rsp['num_ids_p_epost']
        pat_val = {
            'P':epost_rsp['num_ids_p_epost'],
            'F':num_pmids_p_efetch,
            'Qmax':epost_rsp['querykey']}
        for querykey_cur, pmids_cur in enumerate(epost_rsp['qkey2ids'], 1):
            #### if querykey_cur == querykey_max:
            if querykey_cur == querykey_max and querykey_max != 1:
                num_pmids_p_epost_cur = num_pmids%epost_rsp['num_ids_p_epost']
            for start in range(0, num_pmids_p_epost_cur, num_pmids_p_efetch):
                desc = self.pat.format(Q=querykey_cur, S=start, **pat_val)
                # pylint: disable=line-too-long
                pmids_exp = pmids_cur[start:start+num_pmids_p_efetch] if pmids_cur is not None else None
                if pmids_exp:
                    nts.append([desc, start, pmids_exp, querykey_cur])
        return nts

    def _run_efetch(self, database, start, querykey, pmids_exp, desc, **params):
        """Get text from EFetch response"""
        rsp_dct = self.run_req('efetch', retstart=start, query_key=querykey, db=database, **params)
        if rsp_dct is None:
            print(f'\n{desc}\n**ERROR: DATA is None')
            return None
        rsp_txt = rsp_dct['data'].decode('utf-8')
        err_txt = self._chk_error_str(rsp_txt)
        if err_txt is not None:
            print(f'\nURL: {rsp_dct["url"]}\n{desc}\n**ERROR: {err_txt}')
            return None
        ## # PubMed test
        ## pmids_downloaded = [int(i) for i in re.findall(r'PMID-\s*(\d+)', rsp_txt)]
        ## #print(desc, pmids_downloaded, pmids_exp)
        ## if pmids_exp:
        ##     # pylint: disable=line-too-long
        ##     assert pmids_downloaded == pmids_exp, '{TXT}\nDESC: {DESC}\nDL[{D}]: {DL}\nEXP[{L}]: {EXP}'.format(
        ##         TXT=rsp_txt, DESC=desc, D=len(pmids_downloaded),
        ##         DL=pmids_downloaded, EXP=pmids_exp, L=len(pmids_exp))
        return rsp_txt

    @staticmethod
    def _chk_error_str(text):
        """Check if data was correctly downloaded"""
        p0_err = text.find('<ERROR>')
        if p0_err < 0:
            return None
        msg = text[p0_err+7:]
        p1_err = msg.find('</ERROR>')
        return msg[:p1_err]

    #### def pubmed_query_fetch(self, query):
    ####     """Given a PubMed query, return results as  text"""
    ####     rsp_qry = self.find_ids_with_esearch('pubmed', query, retmax=500)
    ####     if rsp_qry is None:
    ####         return {'TEXT':None, 'RSP_QUERY': rsp_qry, 'RSP_POST':None}
    ####     rsp_post = self.epost('pubmed', rsp_qry['idlist'], num_ids_p_epost=10)
    ####     txt = self.run_eutilscmd(
    ####         'efetch',
    ####         db='pubmed',
    ####         retstart=0,
    ####         retmax=500,          # max: 10,000
    ####         rettype='medline',
    ####         retmode='text',
    ####         webenv=rsp_post['webenv'],
    ####         query_key=rsp_post['querykey'])
    ####     return {'TEXT':txt, 'RSP_QUERY': rsp_qry, 'RSP_POST':rsp_post}

    #### def find_ids_with_esearch(self, database, query, retmax, **esearch):
    ####     """Searches an NCBI database for a user search term, returns NCBI IDs."""
    ####     dct = self.run_eutilscmd(
    ####         'esearch',
    ####         db=database,
    ####         term=query,
    ####         retmax=retmax,
    ####         usehistory="y", # NCBI prefers we use history(QueryKey, WebEnv) for next acess
    ####         retmode='json',
    ####         **esearch)

    ####     if dct is not None and 'idlist' in dct and dct['idlist']:
    ####         # KEYS: count retmax retstart querykey webenv idlist
    ####         #       translationset translationstack querytranslation warninglist
    ####         dct['idlist'] = [int(n) for n in dct['idlist']]
    ####         dct['count'] = int(dct['count'])
    ####         # Note: If the maximum number of PMIDs are found, won't get the ones after
    ####         assert len(dct['idlist']) < retmax, 'EntrezUtilities: PMIDS({N}) > retmax({M})'.format(
    ####             M=len(dct['idlist']), N=dct['count'])
    ####         return dct
    ####     return None

    def epost(self, database, ids, num_ids_p_epost=10):
        """Posts to NCBI WebServer of any number of UIDs."""
        # Load the first 1...(step-1) UIDs to entrez-utils using epost. Get WebEnv to finish post
        if not isinstance(ids, list):
            raise RuntimeError(f'\n**FATAL: IDs({ids})\n**FATAL: EPost IDs NOT A LIST')
        if not ids:
            print('**NOTE: NO IDs to EPost')
            return None
        ret = {
            'num_ids_p_epost': num_ids_p_epost,
            'qkey2ids': [ids[:num_ids_p_epost]]
        }
        str_ids = [str(n) for n in ids]
        id_str = ','.join(str_ids[:num_ids_p_epost])
        # epost produces WebEnv value ($web1) and QueryKey value ($key1)
        rsp = self.run_eutilscmd('epost', db=database, id=id_str)
        ## print(f'FFFFFFFFFFFFFFFFFFFFFFFFF EPOST RSP:', rsp)
        if 'webenv' in rsp:
            if self.log is not None:
                ## self.log.write('FIRST EPOST RESULT: {}\n'.format(rsp))
                self.log.write(f'epost webenv: {rsp["webenv"]}\n')
                self.log.write(f"epost querykey({rsp['querykey']:>6}) ids[{len(str_ids)}]={id_str}\n")
            ret['webenv'] = rsp['webenv']
            webenv = rsp['webenv']
            num_ids = len(ids)
            # Load the remainder of the UIDs using epost
            for idx in range(num_ids_p_epost, num_ids, num_ids_p_epost):
                end_pt = idx+num_ids_p_epost
                if num_ids < end_pt:
                    end_pt = num_ids
                #print(f'{num_ids:3} {idx:3} {end_pt:3}')
                id_str = ','.join(str_ids[idx:end_pt])
                rsp = self.run_eutilscmd('epost', db=database, id=id_str, webenv=webenv)
                ret['qkey2ids'].append(ids[idx:idx+num_ids_p_epost])
                webenv = rsp['webenv']
                if self.log is not None:
                    self.log.write(f"epost querykey({rsp['querykey']:>6}) ids[{end_pt-idx}]={id_str}\n")
        elif 'error' in rsp:
            raise RuntimeError(f'**ERROR EPost: {rsp["error"]}\nRESPONSE:\n{rsp}')
        else:
            print(rsp)
            raise RuntimeError(f"NO webenv RETURNED FROM FIRST EPOST\nRESPONSE:\n{rsp}")
        ## if self.log is not None:
        ##     self.log.write('LAST  EPOST RESULT: {}\n'.format(rsp))
        ret['querykey'] = rsp['querykey']
        return ret

    # ------------------------------------------------------------------------------------
    def run_eutilscmd(self, cmd, **params):  # params=None, post=None, ecitmatch=False):
        """Run NCBI E-Utilities command"""
        # params example: db retstart retmax rettype retmode webenv query_key
        ## print('RUN NCBI EUTILS CMD:', cmd)
        ## print('RUN NCBI EUTILS PARAMS:', params)
        rsp_dct = self.run_req(cmd, **params) # post=None, ecitmatch=False):
        ##print('RR run_eutilscmd KEYS RRRRRRRRRRRRRRRRRRR', rsp_dct.keys())
        # dict_keys(['code', 'msg', 'url', 'headers', 'data'])
        ## print('RR run_eutilscmd DATA rsp_dct["data"} RRR', rsp_dct['data'])
        ## print('RR run_eutilscmd rsp_dct RRRRRRRRRRRRRRRR', rsp_dct)
        if rsp_dct is not None:
            return self._extract_rsp(rsp_dct['data'], params.get('retmode'))
        return None

    def _mk_cgi(self, cmd, **params):
        """Get Fast Common Gateway Interface (fcgi) string, given E-utils command/parameters"""
        cgi = self.cgifmt.format(ECMD=cmd)
        ##print('PARAMS', params)
        params = self._construct_params(params)
        options = self._encode_options(params)
        cgi += '?' + options
        return cgi

    def _extract_rsp(self, record, retmode):
        """Extract the data from a response from running a Entrez Utilities command"""
        if retmode == 'json':
            try:
                return json.loads(record)
            except json.decoder.JSONDecodeError as errobj:
                print(f'JSONDecodeError = {str(errobj)}')
                traceback.print_exc()
                print(f'\n**FATAL JSONDecodeError:\n{record.decode("utf-8")}')

        if retmode in {'text', 'asn.1'}:
            ## print('RECORD:', str(record))
            return record.decode('utf-8')

        ## print('XML RETMODE', retmode)   # None
        ## print('XML RECORD', record)     # ePostResult

        # <?xml version="1.0" encoding="ISO-8859-1"?>
        # <!DOCTYPE ePostResult
        #      SYSTEM "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20090526/epost.dtd"
        #      PUBLIC "-//NLM//DTD epost 20090526//EN">
        # <ePostResult>
        #     <QueryKey>1</QueryKey>
        #     <WebEnv>NCID_1_14223415_130.14.18.97 ... </WebEnv>
        # </ePostResult>
        # Parse XML
        root = ElementTree.fromstring(record)
        ## print(f'ElementTree.fromstring(record).root:\n{root}')
        #return root
        assert root.tag in 'ePostResult', f'ElementTree.fromstring(record).tag: {root.tag}'
        ## print('root.tag', root.tag)
        dct = {r.tag.lower():r.text for r in root}
        if 'querykey' in dct:
            dct['querykey'] = int(dct['querykey'])
        ## print('XML root:        ', root)
        ## print('XMLroot.tag:     ', root.tag)
        ## print('XML root.attrib: ', root.attrib)
        ## print('XMLdir(root):    ', dir(root))
        ## print(f'XML[0]({root[0].tag}) ({root[0].text})')
        ## print(f'XML[1]({root[1].tag})')
        ## print('XML dir(root[0]):', dir(root[0]))
        ## print('XML dct:         ', dct)
        return dct

    def run_req(self, cmd, prt=None, **params):  # params=None, post=None, ecitmatch=False):
        """Run NCBI E-Utilities command"""
        # pylint: disable=inconsistent-return-statements
        # params example: db retstart retmax rettype retmode webenv query_key
        cgi = self._mk_cgi(cmd, **params)
        ## print(f'CGI: {cgi}\n')
        try:
            rsp = self._run_req(cgi, prt) # post=None, ecitmatch=False):
            # print('PPPPPPPPPPPPPPPPPP src/pmidcite/eutils/cmds/base.py run_req', rsp)
            return rsp
        except json.decoder.JSONDecodeError as errobj:
            print(f'\n**FATAL: CGI: {cgi}')
            print(f'**FATAL: JSONDecodeError = {str(errobj)}\n')
            traceback.print_exc()
        except urllib.error.HTTPError as errobj:
            print(f'\n**FATAL: CGI: {cgi}')
            print(f'**FATAL: {str(errobj)}\n')
            traceback.print_exc()
        except urllib.error.ContentTooShortError as errobj:
            print(f'\n**FATAL: CGI: {cgi}')
            print(f'**FATAL: ContentTooShortError = {str(errobj.reason)}\n')
            traceback.print_exc()
        except urllib.error.URLError as errobj:
            print(f'\n**FATAL: CGI: {cgi}')
            print(f'**FATAL: URLError = {str(errobj.reason)}\n')
            traceback.print_exc()
        except RuntimeError as errobj:
            print(f'\n**FATAL: CGI: {cgi}\n')
            print(errobj)
            traceback.print_exc()

    def _run_req(self, cgi, prt):  # params=None, post=None, ecitmatch=False):
        """Get a response from running a Entrez Utilities command"""
        # pylint: disable=inconsistent-return-statements
        # NCBI requirement: At most three queries per second if no API key is provided.
        # Equivalently, at least a third of second between queries
        # Using just 0.333333334 seconds sometimes hit the NCBI rate limit,
        # the slightly longer pause of 0.37 seconds has been more reliable.
        delay = 0.1 if self.api_key is not None else 0.37
        current = time.time()
        wait = self.previous + delay - current
        if wait > 0:
            time.sleep(wait)
            self.previous = current + wait
        else:
            self.previous = current
        if prt:
            prt.write(f'CMD: {cgi}\n')
        ## sys.stdout.write('CMD: {CMD}\n'.format(CMD=cgi))  # For PubMed MISMATCHES

        for idx in range(self.max_tries):
            try:
                with urlopen(cgi) as rsp:
                    assert rsp.status == 200, dir(rsp)
                    return {
                        'code': rsp.getcode(),  # code/status
                        'msg': rsp.msg,
                        'url': rsp.geturl(),
                        'headers': cx.OrderedDict(rsp.getheaders()),
                        'data': rsp.read()}
            except _URLError as exception:
                # Reraise if the final try fails
                if idx >= self.max_tries - 1:
                    raise

                # Reraise if the exception is triggered by a HTTP 4XX error
                # indicating some kind of bad request
                if isinstance(exception, _HTTPError): ##? and exception.status // 100 == 4:
                    raise

                # Treat everything else as a transient error and try again after a
                # brief delay.
                time.sleep(self.sleep_between_tries)


    def _construct_params(self, params):
        if params is None:
            params = {}

        # Remove None values from the parameters
        for key, value in list(params.items()):
            if value is None:
                del params[key]
        # Put API key and related info if the researcher has an API key
        if self.api_key is not None:
            if "tool" not in params:
                params["tool"] = self.tool
            # Tell Entrez who we are
            if "email" not in params:
                params["email"] = self.email
            if self.api_key and "api_key" not in params:
                params["api_key"] = self.api_key
        return params

    def _encode_options(self, params):
        """Encode request for url"""
        # If any values in the query arg are sequences and doseq is true, each
        # sequence element is converted to a separate parameter.
        doseq = self._get_doseq(params)
        ## print('DOSEQ', doseq)
        options = urlencode(params, doseq=doseq)
        ## print('ENCODED:', options)
        # urlencode encodes pipes, which NCBI expects in ECitMatch
        if 'ecitmatch' in params:
            options = options.replace("%7C", "|")
        return options

    @staticmethod
    def _get_doseq(params):
        """If doseq==True, each sequence element is converted to a separate parameter"""
        if 'term' in params:
            term = params['term']
            ## print('TERM', term)
            if '[Title]' in term or '[TI]' in term:
                return False
        return True

    @staticmethod
    def _get_num_iterations(count, retmax):
        """Get the number of iterations given the total and the max returned per time"""
        num_tot = count//retmax
        if count%retmax != 0:
            num_tot += 1
        return num_tot


# Copyright (C) 2014-present DV Klopfenstein, PhD. All rights reserved.
