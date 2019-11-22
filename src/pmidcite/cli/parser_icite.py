"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import argparse


# class NIHiCiteArgs:
#     """Manage args for NIH iCite run for one PubMed ID (PMID)"""
# 
#     def __init__(self):
#         self.parser = argparse.ArgumentParser(description='Process some integers.')

def get_argparser():
    """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
    parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
    parser.add_argument('pmids', metavar='PMID', type=int, nargs='*',
        default=[30022098],
        help='PubMed IDs (PMIDs)')
    return parser


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
