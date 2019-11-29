"""Manage command-line args for PMC's ID Converter API"""
# https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import argparse

#from pmidcite.icite.pmid_loader import NIHiCiteLoader
from pmidcite.cfgparser.icite import NIHiCiteCfg
from pmidcite.idconverter.api import IdConverterAPI


class IdConverterCLI:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.cfgparser = NIHiCiteCfg()

    # opt_keys = {
    #     'idtype' : {   # Example:
    #         "pmcid",  # PMC3531190
    #         "pmid",   # 23193287
    #         "mid",    # NIHMS311352
    #         "doi",    # 10.1093/nar/gks1195
    #     },
    #     'format' : {"html", "xml", "json", "csv"},
    #     'version' : {True: "yes", False: "no"},  # Supress versions
    # }

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        self.cfgparser.rd_rc()
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        print(self.cfgparser.cfgfile)
        parser.add_argument(
            'IDs', metavar='ids', type=str, nargs='*',
            help='IDs: pmid, pmcid, mid, or doi')
        parser.add_argument(
            '-t', '--idtype',
            choices=sorted(IdConverterAPI.opt_keys['idtype']),
            help='ID type. PubMed ID (PMID) is the default')
        parser.add_argument(
            '--versions', action='store_true', default=False,
            help="Returns ID versions")
        parser.add_argument(
            '--dir_pmid_py', default=self.cfgparser.cfgparser['DEFAULT']['dir_pmid_py'],
            help='Directory for PMID iCite data stored in Python modules')
        parser.add_argument(
            '--dir_pmid_txt', default=self.cfgparser.cfgparser['DEFAULT']['dir_pmid_txt'],
            help='Directory for PMID data, including the abstract stored in a text file')
        parser.add_argument(
            '-o', '--outfile',
            help='Write report to a ASCII text file')
        #### parser.add_argument(
        ####     '-f', '--force_download', action='store_true',
        ####     help='Download PMID iCite information to a file')
        parser.add_argument(
            '-a', '--append', action='store_true',
            help='Append the current iCite results to the output file, if not already present')
        parser.add_argument(
            '-e', '--echo', action='store_true',
            help='Echo output to screen')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        return parser

    def run(self):
        """Run the argparser"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        print('AAAAAAAAAAAAAAAAAA', args)
        #### if args.generate_rcfile:
        ####     self.cfgparser.wr_rc()
        ####     return
        if not args.IDs:
            argparser.print_help()
            return
        print(args.IDs)
        params = self._get_params(args)
        api = IdConverterAPI(args.dir_pmid_py)
        rsp = api.dnld_ids(args.IDs, **params)
        api.prt_records(rsp, sys.stdout)
        #### loader = NIHiCiteLoader(args.force_download, api, args.references)
        #### print('NIHiCiteArgs WWWWWWWWWWWWWWWW', kws)
        #### if args.outfile is None:
        ####     loader.run_icite_pmids(args.IDs, prtout=sys.stdout)
        #### else:
        ####     if args.echo:
        ####         loader.run_icite_pmids(args.IDs, prtout=sys.stdout)
        ####     if args.append:
        ####         loader.wr_papers(args.outfile, args.IDs, 'a')
        ####     else:
        ####         loader.wr_papers(args.outfile, args.IDs, 'w')

    @staticmethod
    def _get_params(args):
        """Get optional parameters for the PMC ID Converter API"""
        params = {'versions': args.versions}
        if args.idtype is not None:
            params['idtype'] = args.idtype
        return params


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
