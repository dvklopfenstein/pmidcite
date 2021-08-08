"""Groups papers using the NIH percentile"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple


class NihGrouper:
    """Groups papers using the NIH percentile"""

    ntobj = namedtuple('NtNihGroup', 'val txt')

    def __init__(self, group1_min=2.1, group2_min=15.7, group3_min=83.9, group4_min=97.5):
        self.min1 = group1_min
        self.min2 = group2_min
        self.min3 = group3_min
        self.min4 = group4_min

    def get_group(self, nih_percentile):
        """Assign group numbers to the NIH percentile values using the 68-95-99.7 rule"""
        # No NIH percentile yet assigned. This paper should be checked out.
        if nih_percentile is None or nih_percentile == -1:
            return 5
        #  2.1% -3 SD: Very low citation rate
        if nih_percentile < self.min1:  # default: 2.1
            return 0
        # 13.6% -2 SD: Low citation rate
        if nih_percentile < self.min2:  # default: 15.7
            return 1
        # 68.2% -1 SD to +1 SD: Average citation rate
        if nih_percentile < self.min3:  # default: 83.9
            return 2
        # 13.6% +2 SD: High citation rate
        if nih_percentile < self.min4:  # default: 97.5
            return 3
        #  2.1% +3 SD: Very high citation rate
        return 4

    def add_arguments(self, parser):
        """Add NIH grouper arguments to the parser"""
        # pylint: disable=line-too-long
        parser.add_argument(
            '-1', metavar='group1_min', dest='min1', default=self.min1, type=float,
            help='Minimum NIH percentile to be placed in group 1 (default: {D})'.format(D=self.min1))
        parser.add_argument(
            '-2', metavar='group2_min', dest='min2', default=self.min2, type=float,
            help='Minimum NIH percentile to be placed in group 2 (default: {D})'.format(D=self.min2))
        parser.add_argument(
            '-3', metavar='group3_min', dest='min3', default=self.min3, type=float,
            help='Minimum NIH percentile to be placed in group 3 (default: {D})'.format(D=self.min3))
        parser.add_argument(
            '-4', metavar='group4_min', dest='min4', default=self.min4, type=float,
            help='Minimum NIH percentile to be placed in group 4 (default: {D})'.format(D=self.min4))

    def get_list(self):
        """Get the dividing values as a list"""
        return [self.min1, self.min2, self.min3, self.min4]


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
