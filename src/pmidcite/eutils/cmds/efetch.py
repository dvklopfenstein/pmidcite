"""Fetch items and write"""
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch

__author__ = 'DV Klopfenstein, PhD'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved."
__license__ = "GNU AGPLv3"

import sys
import re
from pmidcite.eutils.cmds.cmdbase import CommandBase


class EFetch(CommandBase):
    """Fetch and write text"""

    # pylint: disable=too-many-arguments
    def __init__(self, rettype='medline', retmode='text', batch_size=100):
        retmax = 10000
        super().__init__(retmax, rettype, retmode, batch_size)

    def efetch_and_write(self, ostrm, database, webenv, querykey, num_fetches):
        """EFetch records found for PMIIDs, page by page"""
        ## QueryKey(     1) EFetching(database=pubmed) up to    10 records, starting at 0; ABSTRACT
        ## QueryKey(     1) EFetching(database=pubmed) up to    10 records, starting at 10; ABSTRACT
        ## msg_fmt = ('  QueryKey({:>6}) EFetching(database={}) up to {:5} records, '
        ##            'starting at {}; {}\n')
        for start in range(0, num_fetches, self.batch_size):
            ## msg = msg_fmt.format(querykey, database, self.batch_size, start, self.desc)
            ## sys.stdout.write(msg)
            txt = self.efetch_txt(start, self.batch_size, database, webenv, querykey)

            if txt is not None:
                try:
                    # Read the downloaded data from the socket handle
                    mtch = re.search(r'(ERROR.*\n)', txt)
                    if mtch:
                        sys.stdout.write(mtch.group(1))
                    ostrm.write(txt)
                    ostrm.flush()
                # pylint: disable=broad-except
                except Exception as err:
                    sys.stdout.write(f"*FATAL: BAD READ SOCKET HANDLE: {str(err)}\n")
            else:
                sys.stdout.write("*FATAL: NO SOCKET HANDLE TO READ FROM\n")

    def efetch_txt(self, start, retmax, database, webenv, querykey):
        """Fetch database text"""
        try:
            txt = self.run_eutilscmd(
                'efetch',
                db        = database,
                retstart  = start,         # dflt: 1
                retmax    = retmax,        # max: 10,000
                rettype   = self.rettype,  # Ex: medline
                retmode   = self.retmode,  # Ex: text
                webenv    = webenv,
                query_key = querykey)
            #print('FETCH:', dct)
            return txt
        except IOError as err:
            msg = f"\n*FATAL: EFetching FAILED: {err}"
            sys.stdout.write(msg)
            sys.stdout.write(f"  database:   {database}\n")
            sys.stdout.write(f"  retstart:   {start}\n")
            sys.stdout.write(f"  batch_size: {self.batch_size}\n")
            sys.stdout.write(f"  rettype:    {self.rettype}\n")
            sys.stdout.write(f"  retmode:    {self.retmode}\n")
            sys.stdout.write(f"  webenv:     {webenv}\n")
            sys.stdout.write(f"  querykey:   {querykey}\n")
        return None


# Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved.
