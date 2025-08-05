#!/usr/bin/env python
"""Read a PubMed-generated text file"""

import os.path as op
from pmidcite.eutils.pubmed.rdwr import PubMedRdWr
from pmidcite.eutils.pubmed.author import Author
from tests.utils import get_filename


def test_rd_pubmed():
    """Read a PubMed-generated text file"""
    filename = get_filename("tests/data/pubmed_Kolmogorov2020.txt")
    assert op.exists(filename)
    rdr = PubMedRdWr()
    pmid2info = rdr.get_pmid2info_g_text(filename)
    for pmid, dct in pmid2info.items():
        assert pmid == dct['PMID']
        #_prt_dct(dct)
        assert 'Authors' in dct
        authors_act = dct['Authors'].authors
        authors_exp = _get_exp()
        for act, exp in zip(authors_act, authors_exp):
            assert act == exp, f'UNEXPECTED AUTHOR VALUE:\nACT: {act}\nEXP: {exp}\n'

def _prt_dct(dct):
    for key, val in dct.items():
        print(f"{key:12} {val}")

def _get_exp():
    # pylint: disable=line-too-long
    return [
        Author(
            "Kolmogorov, Mikhail",
            "Kolmogorov M",
            ["Department of Computer Science and Engineering, University of California, San Diego, CA, USA."]),

        Author(
            "Bickhart, Derek M",
            "Bickhart DM",
            ["Cell Wall Biology and Utilization Laboratory, Dairy Forage Research Center, USDA, Madison, WI, USA."]),

        Author(
            "Behsaz, Bahar",
            "Behsaz B",
            ["Graduate Program in Bioinformatics and System Biology, University of California, San Diego, CA, USA."]),

        Author(
            "Gurevich, Alexey",
            "Gurevich A",
            ["Center for Algorithmic Biotechnology, St. Petersburg State University, St. Petersburg, Russia."]),

        Author(
            "Rayko, Mikhail",
            "Rayko M",
            ["Center for Algorithmic Biotechnology, St. Petersburg State University, St. Petersburg, Russia."]),

        Author(
            "Shin, Sung Bong",
            "Shin SB",
            ["USDA-ARS US Meat Animal Research Center, Clay Center, NE, USA."]),

        Author(
            "Kuhn, Kristen",
            "Kuhn K",
            ["USDA-ARS US Meat Animal Research Center, Clay Center, NE, USA."]),

        Author(
            "Yuan, Jeffrey",
            "Yuan J",
            ["Graduate Program in Bioinformatics and System Biology, University of California, San Diego, CA, USA."]),

        Author(
            "Polevikov, Evgeny",
            "Polevikov E",
            ["Center for Algorithmic Biotechnology, St. Petersburg State University, St. Petersburg, Russia.",
            "Bioinformatics Institute, St. Petersburg, Russia."]),

        Author(
            "Smith, Timothy P L",
            "Smith TPL",
            ["USDA-ARS US Meat Animal Research Center, Clay Center, NE, USA."]),

        Author(
            "Pevzner, Pavel A",
            "Pevzner PA",
            ["Department of Computer Science and Engineering, University of California, San Diego, CA, USA. ppevzner@ucsd.edu.",
             "Center for Microbiome Innovation, University of California, San Diego, CA, USA. ppevzner@ucsd.edu."]),
    ]


if __name__ == '__main__':
    test_rd_pubmed()
