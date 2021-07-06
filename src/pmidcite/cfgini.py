"""Configuration file for PMID Cite"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from os.path import exists


PMIDCITERC = \
"""# Link citation data from the National Institute of Health (NIH) to PubMed IDs.

# The file .pmidciterc is a configuration file for the project, pmidcite, and its
# executables, which includes icite.

# To protect your security, store this file (.pmidciterc) in a directory that is
# not managed by git or other version management tools. If the .pmidciterc is in
# the home directory, set the environmental variable, PMIDCITECONF, so pmidcite
# scripts can read it:
#
#   $ export PMIDCITECONF=~/.pmidciterc
#
[pmidcite]

# --------------------------------------------------------------------------------
# Specify the directory to store citation data from the NIH that is downloaded
# using commands such as icite:
#
#  # PMID 33031632 is a new (-1) research (R) paper discussing humans (H)
#  # with 2 citations and 18 references that is authored by 2 (au[02]) people with
#  # the first author being DV Klopfenstein.
#  #
#  $ icite 33031632
#  TOP 33031632 R. H....  -1 i 2021     2  0  18 au[02](D V Klopfenstein) Commentary ...
#
# Thousands of NIH citation files may be downloaded for a literature search
# on a single subject. It is not necessary to save the NIH citation data and I
# recommend not saving these files using git managed from the cloud.
#
# Note: Add an __init__.py file to the ./icite directory
#       Add /icite to the .gitignore to avoid saving thousands of unecessary files using git
#
# Recommended value (mkdir ./icite):
# dir_icite_py = ./icite
dir_icite_py = .

# --------------------------------------------------------------------------------
# Store files containing longer lists of PMIDs into a dedicated directory
# specified using the variable, dir_pmids.
# Files containing lists of PMIDs can be downloaded either from the PubMed GUI
# or by running a PubMed query from your copy of pmidcite's dnld_pmids.py script.
#
# Store NIH citation data for all PMIDs in a single file into a directory
# dedicated to citation data files using the variable, dir_icite.
#
# Recommended values (mkdir ./log; mkdir ./log/pmids; mkdir ./log/icite)
# dir_pmids = ./log/pmids
# dir_icite = ./log/icite
dir_pmids = .
dir_icite = .

# --------------------------------------------------------------------------------
# When comparing numerous papers, use the group variables to place
# the most recent papers first, the highest rated papers next, and
# the lowest-rated papers at the end of the list of papers and citation data.
group1_min = 2.1
group2_min = 15.7
group3_min = 83.9
group4_min = 97.5

# --------------------------------------------------------------------------------
# NCBI E-Utils needs: email, apikey, and tool to download PubMed records.
# These fields are needed if:
#   * You plan to run a search in PubMed and download the resulting list of PMIDs
#   * You plan to download abstracts from NCBI
#
# Note: The fields are not needed for viewing NIH citation data for a given PMID
#
# Learn more about registering for a NCBI API key here:
# https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities
email = name@university.edu
apikey = LONG_HEX_NCBI_API_KEY
tool = scripts

# --------------------------------------------------------------------------------
# Store abstracts and publication data downloaded form PubMed in a dedicated directory
#
# Recommended value (mkdir ./log; mkdir ./log/pubmed):
# dir_pubmed_txt = ./log/pubmed
dir_pubmed_txt = .
"""

def prt_rcfile(prt=stdout):
    """Print a default PMIR icite configuration file"""
    prt.write('\n# == CONFIGURATION FILE BEGIN: .pmidciterc ====================================\n')
    prt.write(PMIDCITERC)
    prt.write('# == CONFIGURATION FILE END: .pmidciterc ======================================\n\n')

def wr_rcfile(cfgfile, force=False):
    """Write a sample configuration with default values set"""
    if not exists(cfgfile) or force:
        with open(cfgfile, 'w') as prt:
            prt.write(PMIDCITERC)
            print('  WROTE: {CFG}'.format(CFG=cfgfile))
            return True
    print('  EXISTS: {CFG} OVERWRITE WITH wr_rc(force=True)'.format(CFG=cfgfile))
    return False


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
