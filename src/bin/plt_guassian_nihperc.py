#!/usr/bin/env python
"""Plot NIH percentile groups for citation data from a paper's cocitation network"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein. All rights reserved."


# pylint: disable=wrong-import-position
import math
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import scipy.stats as stats
from pmidcite.plot.nih_perc import PltNihVals
## from pmidcite.cfg import Cfg

MU = 0
VARIANCE = 1
SIGMA = math.sqrt(VARIANCE)

def main():
    """Plot guassian distribution, showing icite groups"""
    fout_imgs = [
        '../pmidcite/doc/images/nih_perc_groups.png',
        '../bibliometrics/doc/nih_perc_groups.tiff',
        '../bibliometrics/doc/nih_perc_groups.pdf',
        'nih_perc_groups.svg',
        '../bibliometrics/doc/nih_perc_groups.pdf',
    ]

    vlines = [-3, -2, -1, 1, 2, 3]
    probabilities = [round(stats.norm.cdf(z)*100, 2) for z in vlines[1:-1]]
    pltr = PltNihVals(probabilities)
    ## pltr = PltNihVals(Cfg().get_nihgrouper().get_list())
    pltr.prt_vals()

    fig, axes = plt.subplots(1, 1)
    pltr.plt_lines(axes)
    pltr.colorfill_groups(axes)
    pltr.add_text_groups(axes)
    pltr.anno_groupmin(axes)
    axes.set_xlabel('Standard Deviations', fontsize=15)
    axes.set_ylabel('Distribution of co-citation network', fontsize=15)

    for fout_img in fout_imgs:
        fig.tight_layout()
        plt.savefig(fout_img, dpi=800)
        print('WROTE: {IMG}'.format(IMG=fout_img))


if __name__ == '__main__':
    main()

# Copyright (C) 2020-present, DV Klopfenstein. All rights reserved.
