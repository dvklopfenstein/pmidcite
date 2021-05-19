#!/usr/bin/env python3
"""Plot the types of content and their amount in PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.cfg import Cfg
from pmidcite.eutils.pubmed.counts.dnld import PubMedDnld
from pmidcite.eutils.pubmed.counts.plt import PubMedPlot


def main(dnld=False):
    """Plot the types of content and their amount in PubMed"""
    ## fpat_png = 'log/pubmed_content/pubmed_content_{DATE}.png'
    fout_pngs = [
        'pubmed_content_2020_01_10.png',
        'pubmed_content_2020_01_10.tiff',
        'pubmed_content_2020_01_10.pdf',
        'pubmed_content_2020_01_10.pdf',
    ]
    fout_py = 'src/pmidcite/eutils/pubmed/counts/dnlded_data.py'

    cfg = Cfg()
    obj = PubMedDnld(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
    name2cnt, date = obj.get_content_counts(fout_py, dnld)
    # fout_png = fpat_png.format(DATE=date)
    obj.prt_content_counts(name2cnt)
    print('    # {DATE}'.format(DATE=date))

    # Plot PubMed content
    plt = PubMedPlot(name2cnt)
    for fout_png in fout_pngs:
        plt.plt_content_counts(fout_png, dpi=800)
    for name, ntd in plt.dataobj.pltdata_pubmed.items():
        print(' {N:10,} {P:5.1f}% {NAME}'.format(NAME=name, N=ntd.count, P=ntd.perc))


if __name__ == '__main__':
    main(len(sys.argv) != 1)

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
