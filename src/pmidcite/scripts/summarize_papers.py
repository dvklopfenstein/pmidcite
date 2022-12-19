"""Summarize NIH citation data for requested papers from the commandline or in files"""

__copyright__ = "Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from pmidcite.cli.summarize_papers import SummarizePapersCli # get_argparser
from pmidcite.cfg import get_cfgparser


def main():
    """Summarize NIH citation data for requested papers from the commandline or in files"""
    SummarizePapersCli(get_cfgparser(prt=None)).cli()


# Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved.
