"""Fetch items and write"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import sys
import re
from pmidcite.eutils.cmds.cmdbase import CommandBase


# TBD:
class ELink(CommandBase):
    """Fetch and write text"""

    # pylint: disable=too-many-arguments
    def __init__(self, retmax=10000, rettype='medline', retmode='text', batch_size=100, **kws):
        kws_base = {k:v for k, v in kws.items() if k in CommandBase.exp_kws}
        super(ELink, self).__init__(**kws_base)

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
                # pylint: disable=bad-whitespace
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
                msg = "\n*FATAL: EFetching FAILED: {}".format(err)
                sys.stdout.write(msg)
                sys.stdout.write("  database:   {}\n".format(database_from))
                sys.stdout.write("  retstart:   {}\n".format(start))
                # sys.stdout.write("  retmax:     {}\n".format(retmax))
                sys.stdout.write("  batch_size: {}\n".format(self.batch_size))
                sys.stdout.write("  linkname:   {}\n".format(linkname))
                sys.stdout.write("  webenv:     {}\n".format(webenv))
                sys.stdout.write("  querykey:   {}\n".format(querykey))

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
                    sys.stdout.write("*FATAL: BAD READ SOCKET HANDLE: {}\n".format(str(err)))
            else:
                sys.stdout.write("*FATAL: NO SOCKET HANDLE TO READ FROM\n")


# Copyright (C) 2016-present DV Klopfenstein. All rights reserved.
