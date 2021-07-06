"""Plot groups in the NIH percentile map showing how well a paper is doing among its peers"""

__copyright__ = "Copyright (C) 2020-present, Adapted by DV Klopfenstein. All rights reserved."

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
import numpy as np
import scipy.stats as stats
import math
from sys import stdout


class PltNihPercentile:
    """Plot groups in the NIH percentile map showing how well a paper is doing among its peers"""

    MU = 0
    VARIANCE = 1
    SIGMA = math.sqrt(VARIANCE)

    xvals = np.linspace(MU - 3*SIGMA, MU + 3*SIGMA, 120)
    yvals = stats.norm.pdf(xvals, MU, SIGMA)

    def plt_normal_curve(self, axes):
        """Plot the normal curve"""
        axes.plot(self.xvals, self.yvals, color='k')

    def get_vline_yvals(self, div_lines):
        """Get the y-value for the given vertical lines dividing percentile groups"""
        # https://stackoverflow.com/questions/20864847/probability-to-z-score-and-vice-versa
        # zscore-to-percentile: stats.norm.cdf(val)
        # percentile-to-zscore: stats.norm.pdf(val)
        return {xval:stats.norm.pdf(xval, self.MU, self.SIGMA) for xval in div_lines}

    @staticmethod
    def get_colors(colormap):
        """Get colors for each NIH percentile group"""
        cmap = cm.get_cmap(colormap)
        norm = colors.Normalize(vmin=0, vmax=4)
        scalarmap = cm.ScalarMappable(norm=norm, cmap=cmap)
        return [scalarmap.to_rgba(n) for n in range(5)]

    def fill_between(self, axes, xval0, xval1, facecolor):
        """Color between standard deviation lines"""
        xvals = np.linspace(xval0, xval1, 20)
        yvals = stats.norm.pdf(xvals, self.MU, self.SIGMA)
        axes.fill_between(xvals, yvals, facecolor=facecolor, alpha=.4)


class PltNihVals(PltNihPercentile):
    """Plot groups in the NIH percentile map showing how well a paper is doing among its peers"""

    obj = PltNihPercentile()

    def __init__(self, group_dividers):
        self.percentiles = group_dividers  # List of dividers w/values from 0 to 1
        # https://stackoverflow.com/questions/20864847/probability-to-z-score-and-vice-versa
        self.zscores = [stats.norm.ppf(v) for v in group_dividers]
        self.vlines_x = [-3] + self.zscores + [3]
        self.vlines_y = [stats.norm.pdf(x, self.MU, self.SIGMA) for x in self.vlines_x]

    def prt_vals(self, prt=stdout):
        """Print values and their z-scores"""
        for perc, zscore in zip(self.percentiles, self.zscores):
            prt.write('{PERC:5.3f} {Z}\n'.format(PERC=perc, Z=zscore))

    def get_group_percentages(self):
        """Get the percentage that each group represents"""
        vals = [self.percentiles[0],
                self.percentiles[1] - self.percentiles[0],
                self.percentiles[2] - self.percentiles[1],
                self.percentiles[3] - self.percentiles[2],
                1.0 - self.percentiles[3]]
        return [100*v for v in vals]

    def plt_lines(self, axes):
        """Plot the lines bordering the normal distribution and the group dividers"""
        self.plt_normal_curve(axes)
        for xval, yval in zip(self.vlines_x, self.vlines_y):
            axes.vlines(xval, ymin=0, ymax=yval)
        axes.hlines(0, xmin=-3, xmax=3)

    def colorfill_groups(self, axes, colormap='gist_rainbow'):
        """Fill each nih percentile group with a color from the colormap"""
        colors = self.get_colors('gist_rainbow')
        for idx, color in enumerate(colors):
            self.fill_between(axes, self.vlines_x[idx], self.vlines_x[idx+1], color)

    def add_text_groups(self, axes):
        """Add text describing groups and content"""
        group_percs = self.get_group_percentages()
        print(group_percs)
        vals = [int(round(v)) for v in group_percs]
        # 0) Lowest
        axes.text(-2.01, -.003, '0', fontsize=22, ha='right', va='bottom', fontweight='bold')
        # 1) Low
        kwtxt = {'ha':'center', 'va':'center', 'fontweight':'bold'}
        axes.text(-1.24, .12, '1', fontsize=25, **kwtxt)
        axes.text(-1.5, .03, 'Low\n{:2.0f}%'.format(group_percs[1]), fontsize=15, **kwtxt)
        # 2) Good
        axes.text(0, .35, '2', fontsize=25, **kwtxt)
        axes.text(0, .03, 'Good\n{:2.0f}%'.format(group_percs[2]), fontsize=15, **kwtxt)
        # 3) Better
        axes.text(1.24, .12, '3', fontsize=25, **kwtxt)
        axes.text(1.5, .03, 'High\n{:2.0f}%'.format(group_percs[3]), fontsize=15, **kwtxt)
        # 4) Best
        axes.text(2.01, -.003, '4', fontsize=22, ha='left', va='bottom', fontweight='bold')

        axes.annotate('{:2.0f}%'.format(group_percs[0]), fontsize=15, xy=(2.5, 0.02),
                xycoords='data', xytext=(2.7, .07),
                arrowprops=dict(arrowstyle="->",
                                color = 'black'), **kwtxt)
        axes.annotate('{:2.0f}%'.format(group_percs[4]), fontsize=15, xy=(-2.5, 0.02),
                xycoords='data', xytext=(-2.7, .07),
                arrowprops=dict(arrowstyle="->",
                                color = 'black'), **kwtxt)


    def anno_groupmin(self, axes):
        """Add group_minN annotations"""
        axes.annotate('{:2.0f}%'.format(group_percs[0]), fontsize=15, xy=(2.5, 0.02),
        xycoords='data', xytext=(2.7, .07),
        arrowprops=dict(arrowstyle="->",
                        color = 'black'), **kwtxt)



# Copyright (C) 2020-present, Adapted for pmidcite by DV Klopfenstein. All rights reserved.
