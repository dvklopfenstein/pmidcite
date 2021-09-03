"""Default icite arguments"""

from argparse import Namespace

# pylint: disable=line-too-long
ARGS = Namespace(O=False, append_outfile=None, dir_icite='./log/icite', dir_icite_py='None', dir_pubmed_txt='None', force_download=False, force_write=False, generate_rcfile=False, help=False, infile=None, load_citations=False, load_references=False, md=False, min1=2.1, min2=15.7, min3=70.0, min4=97.5, no_references=False, outfile=None, pmids=[1], print_header=False, print_keys=False, pubmed=False, verbose=False)
