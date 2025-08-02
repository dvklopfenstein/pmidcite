"""Plot the types of content and their amount in PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

# pylint: disable=wrong-import-position
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

from pmidcite.eutils.pubmed.counts.data import DataMgr


# pylint: disable=too-few-public-methods
class PubMedPlot:
    """Plot the types of content and their amount in PubMed"""

    arrow_p = {
        'color': 'k',
        'linewidth':0.4,
        'shape':'full',
        'length_includes_head':True,
        'head_width':.3,
        'head_length':400000,
        'head_starts_at_zero': False,
        'overhang':0.0,
        # https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/joinstyle.html
        'capstyle':'butt',    # butt round projecting
        'joinstyle':'bevel',  # miter, round, bevel
    }

    def __init__(self, name2cnt):
        self.name2cnt = name2cnt
        self.dataobj = DataMgr(self.name2cnt)

    def plt_content_counts(self, fout_png, dpi=800):
        """Plot pubmed content"""
        a2n = self.name2cnt
        xmax = a2n['all']
        ymax = 17.5
        # Remove automatically-added 5% axes padding
        mpl.rcParams['axes.autolimit_mode'] = 'data'  # 'data' or 'round_numbers'
        mpl.rcParams['axes.xmargin'] = 0
        mpl.rcParams['axes.ymargin'] = 0
        # Get figure and axes with axes turned off and axes whitespace removed
        fig, axes = plt.subplots()
        fig.set_size_inches(6.4, 1.8)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        axes.set_frame_on(False)
        axes.set_xlim(0, xmax+500000)
        axes.set_ylim(0, ymax+1)
        axes.grid(False)
        # Add horizontal bars for: PubMed, PMC, and other
        bbars = []
        for xvals, yval, dct in self.dataobj.get_pubmed_colorbars(ymax-5):
            print('XY-COORD', xvals, yval)
            bbars.append(axes.broken_barh(xvals, yval, **dct))
        # Add text to colorbars using xy coordinates from 'XY-COORD'
        self._text_on_bars(axes)
        # Add Dimension lines
        # https://schoolworkhelper.net/technical-drawing-alphabet-of-line/
        self._add_bounding_lines_all(xmax, ymax)
        self._add_bounding_lines_medline(a2n['medline_n_inprocess'], ymax-2)
        self._add_bounding_lines_pmc(ymax-6)
        self._add_bounding_lines_other(a2n['all_ml0_pmc0'], ymax-10, xmax)
        self._add_bounding_lines_pmc_100(ymax-12)
        # Add legend
        axes.legend(loc='lower left', fontsize=8, ncol=2,
                    bbox_to_anchor=(0.015, 0.0), borderaxespad=0.1,
                    handletextpad=.2, columnspacing=1.0, labelspacing=.2)
        # Save figure
        plt.savefig(fout_png, bbox_inches='tight', pad_inches=0, dpi=dpi)
        print(f'  WROTE: {fout_png}')

    @staticmethod
    def _text_on_bars(axes):
        """Add text on colorbars using xy coordinates from 'XY-COORD'"""
        dct_txt = {'va':'bottom', 'fontweight':'bold'}
        # bar text: MEDLINE
        # XY-COORD [(       0, 22956376)] (11.5, 1.8)
        # XY-COORD [(22956376,   558119)] (11.5, 1.8)
        # XY-COORD [(23514495,  3505412)] (11.5, 1.8)
        axes.text(22956376*.62, 11.5, 'MEDLINE', fontsize=9, color='white', ha='center', **dct_txt)
        axes.text(22956376*.86, 11.5, 'database', fontsize=9, color='white', ha='center', **dct_txt)
        # pylint: disable=line-too-long
        axes.text(22956376 + 558119 + 3505412*.32, 11.5, '(db)', fontsize=9, color='white', ha='center', **dct_txt)
        # bar text: PMC
        # XY-COORD [(23378342,  136153)] (9.5, 1.8)
        # XY-COORD [(23514495, 3505412)] (9.5, 1.8)
        # XY-COORD [(27019907, 1687687)] (9.5, 1.8)
        axes.text(23514495 + 3505412*.66, 9.5, 'PMC', fontsize=9, color='white', ha='center', **dct_txt)
        axes.text(27019907 + 1687687*.43, 9.5, 'db', fontsize=9, color='white', ha='center', **dct_txt)
        # bar text: other
        # XY-COORD [(28707594, 1819828)] (5.5, 1.8)
        axes.text(28707594+ 1819828/2.0, 5.7, 'Other', fontsize=6.3, color='black', ha='center', **dct_txt)

    def _add_bounding_lines_all(self, xend, ymax):
        """Add bounding lines"""
        plt.plot((0, 0), (ymax-12, ymax+1), color='k', linewidth=0.4)        # LEFT  PubMed LINE
        plt.plot((xend, xend), (ymax-12, ymax+1), color='k', linewidth=0.4)  # RIGHT PubMed LINE
        plt.arrow(4200000, ymax, -4200000, 0, **self.arrow_p)
        plt.arrow(27600000, ymax, xend-27600000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['PubMed']
        txt = f'~{round(ntd.count/1000000.0, 1):4.1f} million (M) citations indexed by PubMed'
        plt.annotate(txt, (4400000, ymax-.5), fontweight='bold')

    def _add_bounding_lines_medline(self, xend, yval):
        """Add bounding lines"""
        plt.plot((xend, xend), (yval-8.7, yval), color='k', linewidth=0.4)   # BLUE-YELLOW DIVIDER
        plt.plot((xend, xend), (yval-14, yval-9.3), color='k', linewidth=0.4)  # BLUE-YELLOW DIVIDER
        plt.arrow(4200000, yval-1, -4200000, 0, **self.arrow_p)
        plt.arrow(16000000, yval-1, xend-16000000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['MEDLINE_n_inprocess']
        txt = f'~{round(ntd.count/1000000.0, 1):4.1f}M ({ntd.perc:4.1f}%) MEDLINE'
        plt.annotate(txt, (4400000, yval-1.5))

    def _add_bounding_lines_pmc(self, yval):
        """Add bounding lines"""
        a2n = self.name2cnt
        # pylint: disable=line-too-long
        #   # PMC
        #   ([(ml2, a2n['inprocess_A_pmc1'])], (23, 1.8), {'facecolors':'tab:cyan', **par}),
        #   ([(ml3, a2n['medline_pmc1'])],     (23, 1.8), {'facecolors':'tab:blue', **par}),
        #   ([(ml4, a2n['pmnml_A_pmc1'] + a2n['pmc_unknown'])], (23, 1.8), {'facecolors':'y', **par}),
        pmc_x0 = a2n['medline_pmc0'] + a2n['inprocess_A_pmc0']
        pmc_all = a2n['pmc_all']
        pmc_xn = pmc_x0 + pmc_all
        plt.plot((pmc_x0, pmc_x0), (yval-2.7, yval+2), color='k', linewidth=0.4)    # UPPER CYAN DIVIDER
        plt.plot((pmc_x0, pmc_x0), (yval-4.7, yval-3.3), color='k', linewidth=0.4)  # UPPER CYAN DIVIDER
        # PMC
        plt.arrow(pmc_x0-9500000, yval-1, 9500000, 0, **self.arrow_p)
        plt.arrow(pmc_xn+1300000, yval-1, -1300000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['PMC']
        txt = f'~{round(ntd.count/1000000.0, 1):5.1f}M ({ntd.perc:3.1f}%) PMC'
        plt.annotate(txt, (4400000, yval-1.5))
        # PMC Only
        plt.arrow(a2n['medline_n_inprocess']-11000000, yval-3, 11000000, 0, **self.arrow_p)
        plt.arrow(pmc_xn+1300000, yval-3, -1300000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['PMC_only']
        txt = f'~{round(ntd.count/1000000.0, 1):5.1f}M (  {ntd.perc:3.1f}%) PMC only'
        plt.annotate(txt, (4400000, yval-3.5))

    def _add_bounding_lines_other(self, other_sz, yval, xmax):
        """Add bounding lines"""
        xval = xmax - other_sz
        plt.plot((xval, xval), (yval-8, yval+4), color='k', linewidth=0.4)  # YELLOW-ORANGE DIVIDER
        plt.arrow(xval-14200000, yval-1, 14200000, 0, **self.arrow_p)
        plt.arrow(xmax+600000, yval-1, -600000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['other']
        txt = f'~{round(ntd.count/1000000.0, 1):5.1f}M ({ntd.perc:5.1f}%) Other'
        plt.annotate(txt, (4400000, yval-1.5))

    def _add_bounding_lines_pmc_100(self, yval):
        """Add bounding lines"""
        a2n = self.name2cnt
        # pylint: disable=line-too-long
        #   # PMC
        #   ([(ml2, a2n['inprocess_A_pmc1'])], (23, 1.8), {'facecolors':'tab:cyan', **par}),
        #   ([(ml3, a2n['medline_pmc1'])],     (23, 1.8), {'facecolors':'tab:blue', **par}),
        #   ([(ml4, a2n['pmnml_A_pmc1'] + a2n['pmc_unknown'])], (23, 1.8), {'facecolors':'y', **par}),
        pmc_all = a2n['pmc_all']
        pmc_ml1 = a2n['medline_pmc1'] + a2n['inprocess_A_pmc1']
        pmc_ml0 = pmc_all - pmc_ml1
        pmc_x0 = a2n['medline_pmc0'] + a2n['inprocess_A_pmc0']
        pmc_x1 = pmc_x0 + pmc_ml1
        pmc_xn = pmc_x0 + pmc_all
        plt.plot((pmc_x0, pmc_x0), (yval-6, yval+0.7), color='k', linewidth=0.4)  # LOWER CYAN DIVIDER
        # PMC AND MEDLINE
        plt.annotate('MEDLINE', (pmc_x0+pmc_ml1/2.0, yval-2.0), ha='center', va='center', fontsize=8)
        # PMC|MEDLINE
        plt.arrow(pmc_x0+900000, yval-3.3, -900000, 0, **self.arrow_p)
        plt.arrow(pmc_x1-900000, yval-3.3, 900000, 0, **self.arrow_p)
        plt.arrow(pmc_xn+700000, yval-3.3, -700000, 0, **self.arrow_p)
        txt_ml1 = f'{round(100.0*pmc_ml1/pmc_all):2.0f}%'
        plt.annotate(txt_ml1, (pmc_x0+pmc_ml1/2.0, yval-3.3), ha='center', va='center', fontsize=8)
        txt_ml0 = f'{round(100.0*(pmc_all-pmc_ml1)/pmc_all):2.0f}%'
        plt.annotate(txt_ml0, (pmc_x1 + pmc_ml0/2.0, yval-3.3), ha='center', va='center', fontsize=8)
        # PMC
        plt.arrow(pmc_x0+1600000, yval-5, -1600000, 0, **self.arrow_p)
        plt.arrow(pmc_xn-1600000, yval-5, 1600000, 0, **self.arrow_p)
        plt.annotate('PMC', (pmc_x0+pmc_all/2.0, yval-5), ha='center', va='center')


# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
