"""ELink"""

__author__ = 'DV Klopfenstein, PhD'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved."
__license__ = "AGPL-3.0"

import sys
import re
from pmidcite.eutils.cmds.base import EntrezUtilities


class ELink(EntrezUtilities):
    """ELink"""

    # pylint: disable=too-many-arguments
    def __init__(self, email, apikey, tool, batch_size=100):
        super().__init__(email, apikey, tool)
        self.batch_size = batch_size

    def elink(self, database_from, linkname, webenv, querykey, num_fetches):
        """EFetch records found for PMIDs, page by page"""
        ## QueryKey(     1) EFetching(database=pubmed) up to    10 records, starting at 0; ABSTRACT
        ## QueryKey(     1) EFetching(database=pubmed) up to    10 records, starting at 10; ABSTRACT
        ## msg_fmt = ('  QueryKey({:>6}) EFetching(database={}) up to {:5} records, '
        ##            'starting at {}; {}\n')
        for start in range(0, num_fetches, self.batch_size):
            ## msg = msg_fmt.format(querykey, database, self.batch_size, start, self.desc)
            ## sys.stdout.write(msg)
            record = None
            try:
                record = self.run_eutilscmd(
                    'elink',
                    db        = database_from,
                    retstart  = start,       # dflt: 1
                    retmax    = self.batch_size,  # max: 10,000
                    retmode   = 'json',
                    linkname  = linkname,
                    webenv    = webenv,
                    query_key = querykey)
                print('ELINK:', linkname, record)
            except IOError as err:
                msg = f"\n*FATAL: EFetching FAILED: {err}"
                sys.stdout.write(msg)
                sys.stdout.write(f"  database:   {database_from}\n")
                sys.stdout.write(f"  retstart:   {start}\n")
                # sys.stdout.write(f"  retmax:     {retmax}\n")
                sys.stdout.write(f"  batch_size: {self.batch_size}\n")
                sys.stdout.write(f"  linkname:   {linkname}\n")
                sys.stdout.write(f"  webenv:     {webenv}\n")
                sys.stdout.write(f"  querykey:   {querykey}\n")

            if record is not None:
                try:
                    # Read the downloaded data from the socket handle
                    mtch = re.search(r'(ERROR.*\n)', record)
                    if mtch:
                        sys.stdout.write(mtch.group(1))
                    # ostrm.write(record)
                    # ostrm.flush()
                # pylint: disable=broad-except
                except Exception as err:
                    sys.stdout.write(f"*FATAL: BAD READ SOCKET HANDLE: {str(err)}\n")
            else:
                sys.stdout.write("*FATAL: NO SOCKET HANDLE TO READ FROM\n")


# Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved.
