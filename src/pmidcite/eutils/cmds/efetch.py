"""Fetch items and write"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import sys
import re
from pmidcite.eutils.cmds.cmdbase import CommandBase


class EFetch(CommandBase):
    """Fetch and write text"""

    # pylint: disable=too-many-arguments
    def __init__(self, retmax=10000, rettype='medline', retmode='text', batch_size=100, **kws):
        kws_base = {k:v for k, v in kws.items() if k in CommandBase.exp_kws}
        super(EFetch, self).__init__(**kws_base)

    def efetch_and_write(self, ostrm, database, webenv, querykey, num_fetches):
        """EFetch records found for PMIIDs, page by page"""
        ## QueryKey(     1) EFetching(database=pubmed) up to    10 records, starting at 0; ABSTRACT
        ## QueryKey(     1) EFetching(database=pubmed) up to    10 records, starting at 10; ABSTRACT
        ## msg_fmt = ('  QueryKey({:>6}) EFetching(database={}) up to {:5} records, '
        ##            'starting at {}; {}\n')
        for start in range(0, num_fetches, self.batch_size):
            ## msg = msg_fmt.format(querykey, database, self.batch_size, start, self.desc)
            ## sys.stdout.write(msg)
            txt = None
            try:
                # pylint: disable=bad-whitespace
                txt = self.run_eutilscmd(
                    'efetch',
                    db        = database,
                    retstart  = start,       # dflt: 1
                    retmax    = self.batch_size,  # max: 10,000
                    rettype   = self.rettype,   # Ex: medline
                    retmode   = self.retmode,      # Ex: text
                    webenv    = webenv,
                    query_key = querykey)
                #print('FETCH:', dct)
            except IOError as err:
                msg = "\n*FATAL: EFetching FAILED: {}".format(err)
                sys.stdout.write(msg)
                sys.stdout.write("  database:   {}\n".format(database))
                sys.stdout.write("  retstart:   {}\n".format(start))
                sys.stdout.write("  batch_size: {}\n".format(self.batch_size))
                sys.stdout.write("  rettype:    {}\n".format(self.rettype))
                sys.stdout.write("  retmode:    {}\n".format(self.retmode))
                sys.stdout.write("  webenv:     {}\n".format(webenv))
                sys.stdout.write("  querykey:   {}\n".format(querykey))

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
                    sys.stdout.write("*FATAL: BAD READ SOCKET HANDLE: {}\n".format(str(err)))
            else:
                sys.stdout.write("*FATAL: NO SOCKET HANDLE TO READ FROM\n")


# Copyright (C) 2016-present DV Klopfenstein. All rights reserved.
