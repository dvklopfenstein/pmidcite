"""Python Wrapper for PMC's ID Converter API"""
# https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import requests

## from pmidcite.icite.entry import NIHiCiteEntry
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
        # This API wrapper supports json
        # 'format' : {"html", "xml", "json", "csv"},
        'versions' : {True: "yes", False: "no"},  # Supress versions
    }

    fmt_idtype = [
        ('pmid', '{VAL:12}'),
        ('doi', '{VAL:20}'),
        ('pmcid', '{VAL:12}'),
        ('mid', '{VAL:14}'),
    ]

    url_base = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
    max_ids = 200

    tf2yn = {True:'yes', False:'no'}

    def __init__(self, dirpy_dnld='.'):
        # EUtilsCfg reads the email, apikey, and tool from file,
        # .eutilsrc needed for the E-utils API
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
        # print('PPPPPPPPPPPPPP', params)
        # TBD: https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n#1625023
        cmd = self._get_cmd(ids, **params)
        print('CCCCCCCCCCCCCCCCCCCCCCC', cmd)
        rsp = requests.get(cmd)
        if rsp.status_code == 200:
            ## print('RRRRRRRRRRRRRRRRRRRRRRRRR', dir(rsp))
            # {
            #     'status': 'ok',
            #     'responseDate': '2019-11-29 09:23:21',
            #     'request': 'ids=8011279;format=json;email=name%40univ.edu;tool=scripts',
            #     'records': [
            #         {
            #             'pmcid': 'PMC6764101',
            #             'pmid': '31560050',
            #             'doi': '10.1093/database/baz110',
            #             'versions': [{'pmcid': 'PMC6764101.1', 'current': 'true'}]
            #         },
            #         {
            #             'pmid':'8011279',
            #             'live':'false', 'status':'error', 'errmsg':'invalid article id'}
            #     ]
            # }
            rsp_json = rsp.json()
            return rsp_json['records']
        ## raise RuntimeError(self._err_msg(rsp))
        print(self._err_msg(rsp))
        return None

    def prt_records(self, records, prt=sys.stdout):
        """Print the records returned from an ID conversion request"""
        for dct in records:
            if 'errmsg' not in dct:
                prt.write('{VALs}\n'.format(VALs=self._str_vals(dct)))
            else:
                self._prt_errmsg(dct, prt)

    def _prt_errmsg(self, dct, prt):
        """Print error message when ID could not be translated"""
        prt.write('**{STATUS}({MSG}): {VALs}\n'.format(
            STATUS=dct['status'].upper(), MSG=dct['errmsg'], VALs=self._str_vals(dct)))

    def _str_vals(self, dct):
        return ' '.join([f.format(VAL=dct[t]) for t, f in self.fmt_idtype if t in dct])


    def _get_cmd(self, ids, **params):
        """Assemble the ID Converter API command"""
        cmd = '{URL}?ids={PMIDS}&format=json&email={EMAIL}&tool={TOOL}'.format(
            URL=self.url_base,
            PMIDS=','.join(str(p) for p in ids),
            EMAIL=self.email,
            TOOL=self.tool)
        if not params:
            return cmd
        option2val = self._get_option2val(**params)
        if not option2val:
            return cmd
        optstr = '&'.join(['{K}={V}'.format(K=k, V=v) for k, v in option2val.items()])
        return '{CMD}&{PARAMS}'.format(CMD=cmd, PARAMS=optstr)

    def _get_option2val(self, **params):
        """Get optional arguments for the ID Converter API command"""
        option2val = {}
        if 'idtype' in params:
            self._set_option2val(params['idtype'], 'idtype', option2val)
        if 'versions' in params:  # Version is a bool
            option2val['versions'] = self.tf2yn[params['versions']]
        return option2val

    def _set_option2val(self, val, key, option2val):
        """Set user-specified val in options, if it is expected"""
        if val in self.opt_keys[key]:
            option2val[key] = val
        else:
            print('**WARNING: UNKNOWN {KEY}({V})'.format(KEY=key, V=val))

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

    ## def _jsonpmid_to_obj(self, json_dct):
    ##     """Given a PMID json dict, return a NIHiCiteEntry object"""
    ##     file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=json_dct['pmid'])
    ##     adj_dct = self._adjust_jsondct(json_dct)
    ##     self.wrpy(file_pmid, adj_dct)
    ##     return NIHiCiteEntry(adj_dct)

    ## def _adjust_jsondct(self, json_dct):
    ##     """Adjust values in the json dict"""
    ##     return json_dct
    ##     #### dct = {}
    ##     #### if 'authors' is not None:
    ##     ####     dct['authors'] = json_dct['authors'].split(', ')
    ##     #### yes_no = self.yes_no
    ##     #### dct['is_research_article'] = yes_no[json_dct['is_research_article']]
    ##     #### dct['is_clinical'] = yes_no[json_dct['is_clinical']]
    ##     #### dct['provisional'] = yes_no[json_dct['provisional']]
    ##     #### lst = []
    ##     #### lists = {'authors', 'cited_by_clin', 'cited_by', 'references'}
    ##     #### for key, val in json_dct.items():
    ##     ####     if key in dct:
    ##     ####         lst.append((key, dct[key]))
    ##     ####     elif key in lists:
    ##     ####         lst.append((key, [] if val is None else val))
    ##     ####     else:
    ##     ####         lst.append((key, val))
    ##     #### return cx.OrderedDict(lst)

    ## def wrpy(self, fout_py, dct):
    ##     """Write NIH iCite to a Python module"""
    ##     with open(fout_py, 'w') as prt:
    ##         self.prt_dct(dct, prt)
    ##         print('  WROTE: {PY}'.format(PY=fout_py))

    ## @staticmethod
    ## def prt_dct(dct, prt=sys.stdout):
    ##     """Print NIH iCite data as a dict"""
    ##     iciteobj = NIHiCiteEntry(dct)
    ##     prt.write('"""Write data downloaded for NIH iCite data"""\n\n')
    ##     prt.write('# disable=line-too-long\n')
    ##     prt.write('# DESC: {DESC}\n'.format(DESC=str(iciteobj)))
    ##     prt.write('ICITE = {\n')
    ##     str_val = {'title', 'journal', 'doi'}
    ##     for key, val in dct.items():
    ##         if key == 'authors':
    ##             prt.write("    '{K}': {V},\n".format(K=key, V=val))
    ##             #prt.write("    '{K}': {AUTHORS},\n".format(
    ##             #    K=key,
    ##             #    AUTHORS='\n'.join(['"{AU}"'.format(AU=a) for a in val])))
    ##         elif key not in str_val:
    ##             prt.write("    '{K}': {V},\n".format(K=key, V=val))
    ##         else:
    ##             prt.write('''    '{K}': """{V}""",\n'''.format(K=key, V=val))
    ##     prt.write('}\n')


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
