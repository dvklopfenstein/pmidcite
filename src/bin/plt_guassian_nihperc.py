#!/usr/bin/env python

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
import numpy as np
import scipy.stats as stats
import math

MU = 0
VARIANCE = 1
SIGMA = math.sqrt(VARIANCE)

def main():
    """Plot guassian distribution, showing icite groups"""
    fout_imgs = [
        '../pmidcite/doc/images/nih_perc_groups.png',
        '../bibliometrics/doc/nih_perc_groups.tiff',
        '../bibliometrics/doc/nih_perc_groups.pdf',
        '../bibliometrics/doc/nih_perc_groups.pdf',
    ]

    vlines = [-3, -2, -1, 1, 2, 3]
    xvals = np.linspace(MU - 3*SIGMA, MU + 3*SIGMA, 120)
    yvals = stats.norm.pdf(xvals, MU, SIGMA)
    x2y = {xvals:stats.norm.pdf(xvals, MU, SIGMA) for xvals in vlines}

    fig, axes = plt.subplots(1, 1)
    axes.plot(xvals, yvals, color='k')
    for xval in vlines:
        plt.vlines(xval, ymin=0, ymax=x2y[xval])
    plt.hlines(0, xmin=-3, xmax=3)

    # Fill with color
    colors = _get_colors('gist_rainbow')
    _fill_between(axes, -3, -2, colors[0])
    _fill_between(axes, -2, -1, colors[1])
    _fill_between(axes, -1, 1, colors[2])
    _fill_between(axes, 1, 2, colors[3])
    _fill_between(axes, 2, 3, colors[4])

    # Add text
    # 0) Lowest
    plt.text(-2.01, -.003, '0', fontsize=22, ha='right', va='bottom', fontweight='bold')
    # 1) Low
    kwtxt = {'ha':'center', 'va':'center', 'fontweight':'bold'}
    plt.text(-1.24, .12, '1', fontsize=25, **kwtxt)
    plt.text(-1.5, .03, 'Low\n14%', fontsize=15, **kwtxt)
    # 2) Good
    plt.text(0, .35, '2', fontsize=25, **kwtxt)
    plt.text(0, .03, 'Good\n68%', fontsize=15, **kwtxt)
    # 3) Better
    plt.text(1.24, .12, '3', fontsize=25, **kwtxt)
    plt.text(1.5, .03, 'High\n14%', fontsize=15, **kwtxt)
    # 4) Best
    plt.text(2.01, -.003, '4', fontsize=22, ha='left', va='bottom', fontweight='bold')

    plt.xlabel('Standard Deviation lines')
    plt.ylabel('Distribution')

    axes.annotate('2%', fontsize=15, xy=(2.5, 0.02),
            xycoords='data', xytext=(2.7, .07),
            arrowprops=dict(arrowstyle="->",
                            color = 'black'), **kwtxt)
    axes.annotate('2%', fontsize=15, xy=(-2.5, 0.02),
            xycoords='data', xytext=(-2.7, .07),
            arrowprops=dict(arrowstyle="->",
                            color = 'black'), **kwtxt)

    for fout_img in fout_imgs:
        plt.savefig(fout_img, dpi=800)
        print('WROTE: {IMG}'.format(IMG=fout_img))

def _get_colors(colormap):
    """Get colors"""
    cmap = cm.get_cmap(colormap)
    norm = colors.Normalize(vmin=0, vmax=4)
    scalarmap = cm.ScalarMappable(norm=norm, cmap=cmap)
    return [scalarmap.to_rgba(n) for n in range(5)]

def _fill_between(axes, xval0, xval1, facecolor):
    """Color between standard deviation lines"""
    xvals = np.linspace(xval0, xval1, 20)
    yvals = stats.norm.pdf(xvals, MU, SIGMA)
    axes.fill_between(xvals, yvals, facecolor=facecolor, alpha=.4)


if __name__ == '__main__':
    main()
