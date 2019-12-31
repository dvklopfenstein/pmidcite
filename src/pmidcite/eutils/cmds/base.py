"""This script downloads NCBI records based on user search query"""

# Entrez Help:
# https://www.ncbi.nlm.nih.gov/books/NBK3837/
#
# A General Introduction to the E-utilities:
# https://www.ncbi.nlm.nih.gov/books/NBK25497/
#
# Entrez Programming Utilities Help:
# http://www.ncbi.nlm.nih.gov/books/NBK25501/
#
# The E-utilities In-Depth: Parameters, Syntax and More:
# http://www.ncbi.nlm.nih.gov/books/NBK25499/
#
# For NCBI's online documentation of efetch:
# http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
#
# tags:
# https://www.ncbi.nlm.nih.gov/books/NBK3827/table/pubmedhelp.Tn/


__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import sys
import traceback
import json
import collections as cx
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
    exp_kws = {'email', 'apikey', 'tool', 'log'}

    max_tries = 3
    sleep_between_tries = 15

    def __init__(self, email, apikey, tool, log=sys.stdout):
        # Cfg reads your email, apikey, and tool from file, .eutilsrc
        # To prevent your API key from being public,
        # don't store .eutilsrc in a public repo.
        #### _cfg = Cfg()
        self.email = email      # _cfg.get_email()
        self.api_key = apikey   # _cfg.get_apikey()
        self.tool = tool        # _cfg.get_tool()
        self.previous = 0
        self.log = log

    def get_database_list(self):
        """Get a list of Entrez databases"""
        # einfo: http://www.ncbi.nlm.nih.gov/books/NBK25499/
        return self.run_eutilscmd('einfo', retmode='json')

    def pubmed_query_fetch(self, query):
        """Given a PubMed query, return results as  text"""
        rsp_qry = self.find_ids_with_esearch('pubmed', query, retmax=500)
        if rsp_qry is None:
            return {'TEXT':None, 'RSP_QUERY': rsp_qry, 'RSP_POST':None}
        rsp_post = self.epost('pubmed', rsp_qry['idlist'], num_ids_p_epost=10)
        txt = self.run_eutilscmd(
            'efetch',
            db='pubmed',
            retstart=0,
            retmax=500,          # max: 10,000
            rettype='medline',
            retmode='text',
            webenv=rsp_post['webenv'],
            query_key=rsp_post['querykey'])
        return {'TEXT':txt, 'RSP_QUERY': rsp_qry, 'RSP_POST':rsp_post}

    def find_ids_with_esearch(self, database, query, retmax, **esearch):
        """Searches an NCBI database for a user search term, returns NCBI IDs."""
        dct = self.run_eutilscmd(
            'esearch',
            db=database,
            term=query,
            retmax=retmax,
            usehistory="y", # NCBI prefers we use history(QueryKey, WebEnv) for next acess
            retmode='json',
            **esearch)

        if dct is not None and 'idlist' in dct and dct['idlist']:
            # KEYS: count retmax retstart querykey webenv idlist
            #       translationset translationstack querytranslation warninglist
            dct['idlist'] = [int(n) for n in dct['idlist']]
            dct['count'] = int(dct['count'])
            # Note: If the maximum number of PMIDs are found, won't get the ones after
            assert len(dct['idlist']) < retmax, 'EntrezUtilities: PMIDS({N}) > retmax({M})'.format(
                M=len(dct['idlist']), N=dct['count'])
            return dct
        return None

    def epost(self, database, pmids, num_ids_p_epost=10):
        """Posts to NCBI WebServer of any number of UIDs."""
        # Load the first 1...(step-1) UIDs to entrez-utils using epost. Get WebEnv to finish post
        if not isinstance(pmids, list):
            raise RuntimeError('**FATAL: EPost PMIDs MUST BE IN A LIST')
        if not pmids:
            print('**NOTE: NO PMIDs to EPost')
            return None
        ret = {
            'num_ids_p_epost': num_ids_p_epost,
            'qkey2ids': [pmids[:num_ids_p_epost]]
        }
        str_ids = [str(n) for n in pmids]
        id_str = ','.join(str_ids[:num_ids_p_epost])
        # epost produces WebEnv value ($web1) and QueryKey value ($key1)
        rsp = self.run_eutilscmd('epost', db=database, id=id_str)
        if 'webenv' in rsp:
            if self.log is not None:
                ## self.log.write('FIRST EPOST RESULT: {}\n'.format(rsp))
                self.log.write('epost webenv: {W}\n'.format(W=rsp['webenv']))
                self.log.write("epost querykey({Q:>6}) pmids[{N}]={Ps}\n".format(
                    N=len(str_ids), Q=rsp['querykey'], Ps=id_str))
            ret['webenv'] = rsp['webenv']
            webenv = rsp['webenv']
            num_ids = len(pmids)
            # Load the remainder of the UIDs using epost
            for idx in range(num_ids_p_epost, num_ids, num_ids_p_epost):
                end_pt = idx+num_ids_p_epost
                if num_ids < end_pt:
                    end_pt = num_ids
                #print '{:3} {:3} {:3}'.format(num_ids, idx, end_pt)
                id_str = ','.join(str_ids[idx:end_pt])
                rsp = self.run_eutilscmd('epost', db=database, id=id_str, webenv=webenv)
                ret['qkey2ids'].append(pmids[idx:idx+num_ids_p_epost])
                webenv = rsp['webenv']
                if self.log is not None:
                    self.log.write("epost querykey({Q:>6}) pmids[{N}]={Ps}\n".format(
                        N=end_pt-idx, Q=rsp['querykey'], Ps=id_str))
        elif 'error' in rsp:
            raise RuntimeError('**ERROR EPost: {MSG}'.format(MSG=rsp['error']))
        else:
            print(rsp)
            raise Exception("NO webenv RETURNED FROM FIRST EPOST")
        ## if self.log is not None:
        ##     self.log.write('LAST  EPOST RESULT: {}\n'.format(rsp))
        ret['querykey'] = rsp['querykey']
        return ret

    @staticmethod
    def _return_einforesult(record):
        """Return EInfo result"""
        einforesult = record['einforesult']
        cmdtype = record['header']['type']
        if 'dblist' in einforesult:
            return einforesult['dblist']
        if cmdtype == 'einfo' and 'dbinfo' in einforesult:
            assert len(record['einforesult']['dbinfo']) == 1
            ## print('RRRRRRRRRRRRRRR', record.keys())
            ## print('RRRRRRRRRRRRRRR', len(record['einforesult']['dbinfo']))
            ## print('RRRRRRRRRRRRRRR', record)
            return record['einforesult']['dbinfo'][0]
        raise RuntimeError('IMPLEMENT _return_einforesult')

    @staticmethod
    def _return_linksets(record):
        """Return ELink result"""
        links_all = []
        for dct0 in record['linksets']:
            ## print('DCT', dct0)
            if 'linksetdbs' in dct0:
                for dct1 in dct0['linksetdbs']:
                    links_all.extend(dct1['links'])
        print('{N} LINKED ITEMS'.format(N=len(links_all)))
        return links_all

    # ------------------------------------------------------------------------------------
    def run_eutilscmd(self, cmd, **params):  # params=None, post=None, ecitmatch=False):
        """Run NCBI E-Utilities command"""
        # params example: db retstart retmax rettype retmode webenv query_key
        rsp_dct = self.run_req(cmd, **params) # post=None, ecitmatch=False):
        rcvd = self._extract_rsp(rsp_dct['data'], params.get('retmode'))
        return rcvd

    def _mk_cgi(self, cmd, **params):
        """Get Fast Common Gateway Interface (fcgi) string, given E-utils command/parameters"""
        cgi = self.cgifmt.format(ECMD=cmd)
        params = self._construct_params(params)
        ## print('PARAMS', params)
        options = self._encode_options(params)
        cgi += '?' + options
        return cgi

    def run_req(self, cmd, **params):  # params=None, post=None, ecitmatch=False):
        """Run NCBI E-Utilities command"""
        # params example: db retstart retmax rettype retmode webenv query_key
        cgi = self._mk_cgi(cmd, **params)
        ## print('CGI: {CGI}\n'.format(CGI=cgi))
        try:
            return self._run_req(cgi) # post=None, ecitmatch=False):
        except json.decoder.JSONDecodeError as errobj:
            print('CGI: {CGI}\n'.format(CGI=cgi))
            print('JSONDecodeError = {ERR}'.format(ERR=str(errobj)))
            traceback.print_exc()
        except urllib.error.HTTPError as errobj:
            print('CGI: {CGI}\n'.format(CGI=cgi))
            print('HTTPError = {ERR}'.format(ERR=str(errobj.code)))
            traceback.print_exc()
        except urllib.error.ContentTooShortError as errobj:
            print('CGI: {CGI}\n'.format(CGI=cgi))
            print('ContentTooShortError = {ERR}'.format(ERR=str(errobj.reason)))
            traceback.print_exc()
        except urllib.error.URLError as errobj:
            print('CGI: {CGI}\n'.format(CGI=cgi))
            print('URLError = {ERR}'.format(ERR=str(errobj.reason)))
            traceback.print_exc()
        except RuntimeError as errobj:
            print('CGI: {CGI}\n'.format(CGI=cgi))
            print(errobj)
            traceback.print_exc()

    def _run_req(self, cgi):  # params=None, post=None, ecitmatch=False):
        """Get a response from running a Entrez Utilities command"""
        # NCBI requirement: At most three queries per second if no API key is provided.
        # Equivalently, at least a third of second between queries
        # Using just 0.333333334 seconds sometimes hit the NCBI rate limit,
        # the slightly longer pause of 0.37 seconds has been more reliable.
        delay = 0.1 if self.api_key else 0.37
        current = time.time()
        wait = self.previous + delay - current
        if wait > 0:
            time.sleep(wait)
            self.previous = current + wait
        else:
            self.previous = current

        for i in range(self.max_tries):
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
                if i >= self.max_tries - 1:
                    raise

                # Reraise if the exception is triggered by a HTTP 4XX error
                # indicating some kind of bad request
                if isinstance(exception, _HTTPError): ##? and exception.status // 100 == 4:
                    raise

                # Treat everything else as a transient error and try again after a
                # brief delay.
                time.sleep(self.sleep_between_tries)

    def _extract_rsp(self, record, retmode):
        """Extract the data from a response from running a Entrez Utilities command"""
        if retmode == 'json':
            try:
                dct = json.loads(record)
                if 'esearchresult' in dct:
                    return dct['esearchresult']
                if 'einforesult' in dct:
                    return self._return_einforesult(dct)
                if 'linksets' in dct:
                    return self._return_linksets(dct)
                print('KEYS:', dct.keys())
                print('DCT:', dct)
                raise RuntimeError('UNKNOWN RESULT in _run_req')
            except json.decoder.JSONDecodeError as errobj:
                print('JSONDecodeError = {ERR}'.format(ERR=str(errobj)))
                traceback.print_exc()
                print('\n**FATAL JSONDecodeError:\n{RECORD}'.format(RECORD=record.decode('utf-8')))

        if retmode == 'text':
            ## print('RECORD:', str(record))
            return record.decode('utf-8')

        ## print('RETMODE', retmode)
        ## print('RECORD', record)

        ## print(record)
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
        ## print('root.tag', root.tag)
        assert root.tag in 'ePostResult', root.tag
        dct = {r.tag.lower():r.text for r in root}
        if 'querykey' in dct:
            dct['querykey'] = int(dct['querykey'])
        ## print('XML:', root)
        ## print('XML:', root.tag)
        ## print('XML:', root.attrib)
        ## print('XML:', dir(root))
        ## print('XML[0]({}) ({})'.format(root[0].tag, root[0].text))
        ## print('XML[1]({})'.format(root[1].tag))
        ## print('XML:', dir(root[0]))
        ## print('XML:', dct)
        return dct

    def _construct_params(self, params):
        if params is None:
            params = {}

        # Remove None values from the parameters
        for key, value in list(params.items()):
            if value is None:
                del params[key]
        # Tell Entrez that we are using Biopython (or whatever the user has
        # specified explicitly in the parameters or by changing the default)
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


# Copyright (C) 2014-present DV Klopfenstein. All rights reserved.
