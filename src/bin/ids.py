#!/usr/bin/env python3
"""Run PMC's ID Converter CLI from the command-line"""
# https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cli.idconverter import IdConverterCLI


def main():
    """Print lists of pubs in formation"""
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
    argobj = IdConverterCLI()
    argobj.run()


if __name__ == '__main__':
    main()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
