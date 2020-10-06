"""Plot the types of content and their amount in PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

from pmidcite.eutils.pubmed.counts.data import DataMgr


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
        print('  WROTE: {PNG}'.format(PNG=fout_png))

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

    def chk_content_counts(self):
        """Check the content typename and the count of that type"""
        a2n = self.name2cnt
        assert a2n['nihms_pub0'] + a2n['nihms_pub1'] == a2n['nihms']
        assert a2n['pmcsd_pmc0'] + a2n['pmcsd_pmc1'] == a2n['pmcsd']
        assert a2n['medline_pmc0'] + a2n['medline_pmc1'] == a2n['medline_all']
        #    557,390 inprocess_A_all      inprocess[sb]
        #    422,103 inprocess_A_pmc0     inprocess[sb] NOT pubmed pmc[sb]
        #    135,287 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
        #    557,390 inprocess_ml0        inprocess[sb] NOT medline[sb]
        #          0 inprocess_ml1        inprocess[sb] AND medline[sb]
        assert a2n['inprocess_A_all'] == a2n['inprocess_A_pmc0'] + a2n['inprocess_A_pmc1']
        # 30,514,237 all          all [sb]
        #  1,818,474 all_ml0_pmc0 all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]
        # 28,695,763 ml1_pmc1     inprocess[sb] OR medline[sb] OR pubmed pmc[sb]
        assert a2n['all'] == a2n['all_ml0_pmc0'] + a2n['ml1_pmc1']
        #  3,116,339 pmnml_A              pubmednotmedline[sb]
        #  3,116,339 pmnml_B              pubmednotmedline[sb] NOT medline[sb]
        #  3,116,339 pmnml_C_ip0          pubmednotmedline[sb] NOT inprocess[sb]
        #          0 pmnml_0_ip1          pubmednotmedline[sb] AND inprocess[sb]
        #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
        #  1,504,065 pmnml_A_pmc0         pubmednotmedline[sb] NOT pubmed pmc[sb]
        assert a2n['pmnml_A'] == a2n['pmnml_A_pmc1'] + a2n['pmnml_A_pmc0']
        #  5,323,939 pmc_all              pubmed pmc[sb]
        #    135,287 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
        #  3,503,057 medline_pmc1         medline[sb] AND pubmed pmc[sb]
        #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
        pmc_notmedline = a2n['pmc_all'] - a2n['medline_pmc1'] - a2n['inprocess_A_pmc1']
        print('  {N:10,} of {M:10,} PMC (not MEDLINE)'.format(M=a2n['pmc_all'], N=pmc_notmedline))
        print(pmc_notmedline - a2n['pmnml_A_pmc1'])
        print('  {N:10,} of {M:10,} PubMed(not MEDLINE, PMC)'.format(
            N=a2n['all_ml0_pmc0'], M=a2n['all']))
        print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
            T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
            A=a2n['ml1_pmc1'],
            B=a2n['all_ml0_pmc0']))
        total = a2n['all']
        au_all = a2n['au_all']
        print('  {N:10,} of {M:10,} {P:3.5f}% author ms'.format(
            N=au_all, M=total, P=100.0*au_all/total))
        print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
            T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
            A=a2n['ml1_pmc1'],
            B=a2n['all_ml0_pmc0']))

    def _add_bounding_lines_all(self, xend, ymax):
        """Add bounding lines"""
        plt.plot((0, 0), (ymax-12, ymax+1), color='k', linewidth=0.4)        # LEFT  PubMed LINE
        plt.plot((xend, xend), (ymax-12, ymax+1), color='k', linewidth=0.4)  # RIGHT PubMed LINE
        plt.arrow(4200000, ymax, -4200000, 0, **self.arrow_p)
        plt.arrow(27600000, ymax, xend-27600000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['PubMed']
        txt = '~{N:4.1f} million (M) citations indexed by PubMed'.format(
            N=round(ntd.count/1000000.0, 1))
        plt.annotate(txt, (4400000, ymax-.5), fontweight='bold')

    def _add_bounding_lines_medline(self, xend, yval):
        """Add bounding lines"""
        plt.plot((xend, xend), (yval-8.7, yval), color='k', linewidth=0.4)   # BLUE-YELLOW DIVIDER
        plt.plot((xend, xend), (yval-14, yval-9.3), color='k', linewidth=0.4)  # BLUE-YELLOW DIVIDER
        plt.arrow(4200000, yval-1, -4200000, 0, **self.arrow_p)
        plt.arrow(16000000, yval-1, xend-16000000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['MEDLINE_n_inprocess']
        txt = '~{N:4.1f}M ({P:4.1f}%) MEDLINE'.format(N=round(ntd.count/1000000.0, 1), P=ntd.perc)
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
        txt = '~{N:5.1f}M ({P:3.1f}%) PMC'.format(N=round(ntd.count/1000000.0, 1), P=ntd.perc)
        plt.annotate(txt, (4400000, yval-1.5))
        # PMC Only
        plt.arrow(a2n['medline_n_inprocess']-11000000, yval-3, 11000000, 0, **self.arrow_p)
        plt.arrow(pmc_xn+1300000, yval-3, -1300000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['PMC_only']
        txt = '~{N:5.1f}M (  {P:3.1f}%) PMC only'.format(N=round(ntd.count/1000000.0, 1), P=ntd.perc)
        plt.annotate(txt, (4400000, yval-3.5))

    def _add_bounding_lines_other(self, other_sz, yval, xmax):
        """Add bounding lines"""
        xval = xmax - other_sz
        plt.plot((xval, xval), (yval-8, yval+4), color='k', linewidth=0.4)  # YELLOW-ORANGE DIVIDER
        plt.arrow(xval-14200000, yval-1, 14200000, 0, **self.arrow_p)
        plt.arrow(xmax+600000, yval-1, -600000, 0, **self.arrow_p)
        ntd = self.dataobj.pltdata_pubmed['other']
        txt = '~{N:5.1f}M ({P:5.1f}%) Other'.format(N=round(ntd.count/1000000.0, 1), P=ntd.perc)
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
        txt_ml1 = '{P:2.0f}%'.format(P=round(100.0*pmc_ml1/pmc_all))
        plt.annotate(txt_ml1, (pmc_x0+pmc_ml1/2.0, yval-3.3), ha='center', va='center', fontsize=8)
        txt_ml0 = '{P:2.0f}%'.format(P=round(100.0*(pmc_all-pmc_ml1)/pmc_all))
        plt.annotate(txt_ml0, (pmc_x1 + pmc_ml0/2.0, yval-3.3), ha='center', va='center', fontsize=8)
        # PMC
        plt.arrow(pmc_x0+1600000, yval-5, -1600000, 0, **self.arrow_p)
        plt.arrow(pmc_xn-1600000, yval-5, 1600000, 0, **self.arrow_p)
        plt.annotate('PMC', (pmc_x0+pmc_all/2.0, yval-5), ha='center', va='center')


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
