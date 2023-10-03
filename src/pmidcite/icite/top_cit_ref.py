"""Manage paper labels: TOP CIT CLI REF"""

__copyright__ = "Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"


class TopCitRef:
    """Manage paper labels: TOP CIT CLI REF"""

    label_list = [
        'TOP',  # Paper of interest
        'CIT',  # A paper (not a clinical study) citing the paper of interest
        'CLI',  # A clinical study paper citing the paper of interest
        'REF',  # A paper in the reference list of the paper of interest
    ]

    label_set = set(label_list)

    choices = label_list + ['CITS', 'ALL']

    def add_arguments(self, parser):
        """Manage paper labels arguments: TOP CIT CLI REF"""
        # pylint: disable=line-too-long
        parser.add_argument(
            '-p', metavar='labels', dest='paper_labels', type=str, nargs='*',
            default=['TOP',],
            choices=self.choices,
            help=f'Paper label choices: {" ".join(self.choices)} (default: TOP)',
        )

    def adjust_args(self, args_paper_labels):
        """Given labels and aliases (CITS, ALL), return official label names"""
        if not args_paper_labels:
            return None
        ret = set()
        arg_set = set(args_paper_labels)
        if 'ALL' in arg_set:
            ret.update(self.label_list)
            return ret
        if 'CITS' in arg_set:
            ret.add('CIT')
            ret.add('CLI')
        ret.update(arg_set.intersection(self.label_list))
        return ret


# Copyright (C) 2022-present DV Klopfenstein, PhD. All rights reserved.
