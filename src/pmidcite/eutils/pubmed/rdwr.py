"""Write Python module for downloaded abstracts."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import os
import datetime

from re import match
from re import search
from pmidcite.eutils.pubmed.terms import MeshTerms
from pmidcite.eutils.pubmed.authors import Authors


class PubMedRdWr:
    """Read downloaded PMID text file [FILE].Entrez_downloads. Write subset into Python module."""

    # https://www.nlm.nih.gov/bsd/mms/medlineelements.html
    flds = [
        'TI',  # Title
        'LID', # Location Identifier
        'AID', # Article Identifier
        'PMC', # PubMed Central Identifier
        'OWN', # Owner
        'STATUS', # Status
        'DP',  # Date of Publication
        'AB',  # Abstract
        'JT',  # Journal Title
        'TA',  # Journal Title abbreviation
        'PT',  # Publication Type
        'MH',  # MeSH Terms
        'FAU', # Full Author
        'AU',  # Author
        'AD',  # Affiliation
        'OTO', # Other Term Owner
        'OT',  # Other Term
    ]

    # pylint: disable=bad-continuation
    _lendate2fmt = { # PMID date formats: "2017 Mar 02"
         4 : "%Y",
         8 : "%Y %b",
         9 : "%Y %b.",
        10 : "%Y %b %d",
        11 : "%Y %b %d"}


    status = {
        'In-Data-Review',
        'In-Process',
        'MEDLINE',
        'OLDMEDLINE',
        'PubMed-not-MEDLINE',
        'Publisher',
    }

    owner = {
        'KIE': 'Kennedy Institute of Ethics, Georgetown University',
        'NASA': 'National Aeronautics and Space Administration',
        'NLM': 'National Library of Medicine (used for the OLDMEDLINE records)',
        'NOTNLM': ('(The journal publisher or other data provider. '
                   'This is used when the OT field includes author-supplied keywords. '
                   'NLM began using this value in January 2013.'),
        'PIP': ('Population Information Program, '
                'Johns Hopkins School of Public health '
                '(not a current value; only on older citations)'),
        'HSR': ('National Information Center on '
                'Health Services Research and Health Care Technology, '
                'National Library of Medicine'),
        'HMD': 'History of Medicine Division, National Library of Medicine',
        'SIS': ('Specialized Information Services Division, '
                'National Library of Medicine '
                '(not yet used; reserved for possible future use)'),
    }

    join_these = {
        'TI':' ', # separate by one space when joining
        'DP':'',  # There is only one, but convert from list to str
        'AB':' ',
        'JT':' ',
        'TA':' ',
        'AD':' ', # Author affiliation(s) Each one can be multiple lines
    }

    def __init__(self):
        # These are one block of text, which may be spread over multiple lines
        self.dates = ['DP']
        self.objmh = MeshTerms()
        self.field2fnc = {
            'PMID': self._to_int,
            'MH': self._fld_add_to_list,
            # Indentifiers
            'LID': self._lid_add_to_dict,
            'AID': self._lid_add_to_dict,
            # Date of Publication
            'DP': self._init_date,
            # Author fields
            'FAU': self._add_author,
            'AU': self._add_author,
            'AD': self._add_author
        }

    def _get_fldobjs_all(self, pmid2fldlines):
        """Given a list of lines in a PubMed entry, return objects."""
        pmid2fldobjs = {}
        for pmid, fldlines in pmid2fldlines.items():
            pmid2fldobjs[pmid] = self._get_fldobjs_one(fldlines, pmid)
        return pmid2fldobjs

    def _get_fldobjs_one(self, fldlines, pmid):
        """Given a list of lines in a PubMed entry, return objects."""
        fld2objs = {}
        field2fnc = self.field2fnc
        for fld, line in fldlines:
            # Mesh Terms
            line = " ".join(line)
            if fld in field2fnc:
                field2fnc[fld](fld2objs, fld, line, pmid)
            else:
                fld2objs[fld] = line
            # Author list
            if fld == 'AU':
                self._fld_add_to_list(fld2objs, fld, line, pmid)
        # die
        return fld2objs

    # pylint: disable=unused-argument
    @staticmethod
    def _to_int(fld2objs, fld, line, pmid):
        """Add a value to a list."""
        fld2objs[fld] = int(line)

    @staticmethod
    def _add_author(fld2objs, fld, line, pmid):
        """Add a value to a list."""
        if 'Authors' not in fld2objs:
            fld2objs['Authors'] = Authors()
        fld2objs['Authors'].add_fld(fld, line, pmid)

    @staticmethod
    def _fld_add_to_list(fld2objs, fld, line, pmid):
        """Add a value to a list."""
        if fld not in fld2objs:
            fld2objs[fld] = []
        fld2objs[fld].append(line)

    @staticmethod
    def _lid_add_to_dict(fld2objs, fld, line, pmid):
        """Add a value to a list."""
        if fld not in fld2objs:
            fld2objs[fld] = {}
        key0 = line.rfind('[')
        # TBD Change these fatals to messages
        assert key0 != -1, '**FATAL LID: {} {}'.format(fld, line)
        assert line[-1] == ']', '**FATAL LID: {} {}'.format(fld, line)
        key = line[key0 + 1:-1]
        val = line[:key0].strip()
        assert key not in fld2objs, '**FATAL LID: {} {} {}'.format(key, val, fld2objs)
        fld2objs[fld][key] = val

    def read_pmid2obj_g_fins(self, fins_pubmed, prt=sys.stdout):
        """Load PubMed objects from text files"""
        pmid2obj = {}
        s_get_pmid2info_g_text = self.get_pmid2info_g_text
        for fin_pubmed in fins_pubmed:
            pmid2fld2obj = s_get_pmid2info_g_text(fin_pubmed, prt=prt)
            for pmid, dct in pmid2fld2obj.items():
                pmid2obj[pmid] = dct
        return pmid2obj

    def get_pmid2info_g_text(self, fin_text, flds=None, dochk=False, prt=sys.stdout):
        """Given file of retmode=text, get data (in flds list) as a python dict."""
        if flds is None:
            flds = self.flds
        # Field list: https://www.nlm.nih.gov/bsd/mms/medlineelements.html
        if os.path.exists(fin_text):
            if prt:
                prt.write("  READING: {PUBMED}\n".format(PUBMED=fin_text))
            with open(fin_text) as ifstrm:
                pmid2fldlines = ProcessLines(flds).process_rawlines(ifstrm)
                pmid2fld2objs = self._get_fldobjs_all(pmid2fldlines)
                if prt:
                    prt.write("  READ  {:>7,} PubMed records {} for fields({})\n".format(
                    len(pmid2fld2objs), fin_text, " ".join(flds)))
                if pmid2fld2objs:
                    if dochk:
                        self._chk(pmid2fld2objs)
                return pmid2fld2objs
        else:
            print("  READ  -- 0 -- PubMed record {}".format(fin_text))
            return {}

    def get_pmid2info_g_textblock(self, textblock, flds=None, dochk=False, prt=sys.stdout):
        """Given file of retmode=text, get data (in flds list) as a python dict."""
        if flds is None:
            flds = self.flds
        # Field list: https://www.nlm.nih.gov/bsd/mms/medlineelements.html
        if textblock:
            pmid2fldlines = ProcessLines(flds).process_rawlines(textblock.split('\n'))
            pmid2fld2objs = self._get_fldobjs_all(pmid2fldlines)
            if prt:
                prt.write("  PROCESSED  {P:>7,} PubMed records for fields({Fs})\n".format(
                    P=len(pmid2fld2objs), Fs=" ".join(flds)))
            if pmid2fld2objs:
                if dochk:
                    self._chk(pmid2fld2objs)
            return pmid2fld2objs
        print("  **WARNING: BAD TEXT: {TXT}".format(TXT=textblock))
        return {}

    def _chk(self, pmid2flds):
        """Ensure that MeSH terms are correct."""
        chk_mhs = self.objmh.chk_mhs
        for fld2vals_raw in pmid2flds.values():
            for fld, vals in fld2vals_raw.items():
                if fld == "MH":
                    chk_mhs(vals)

    def wrpy_pmid2flds(self, fout_py, pmid2info, flds=None, pydoc=None):
        """Write PMID info into Python module."""
        import PyBiocode.Utils.dnld as DL
        if flds is None:
            flds = self.flds
        if pydoc is None:
            pydoc = "PMIDs associated with genes in clusters: {FLDS}".format(FLDS=" ".join(flds))
        num_pmids = len(pmid2info)
        with open(fout_py, 'w') as prt:
            prt.write('"""{DESC}"""\n\n'.format(DESC=pydoc))
            prt.write("# {COPYRIGHT}\n\n".format(COPYRIGHT=DL.get_copyright()))
            prt.write("import datetime\n\n")
            prt.write('downloaded = "{DATE}" # {N} items\n\n'.format(
                N=num_pmids, DATE=DL.get_date()))
            prt.write('num_items = {N}\n\n'.format(N=num_pmids))
            prt.write('pmid2info = {\n')
            #### addquot = lambda valstr: ''.join(["'", valstr, "'"])
            for pmid, fld2val_all in self._wrpy_get_sorted(pmid2info, flds):
                fld2val_cur = self._get_fld2val_cur(fld2val_all, flds)
                if fld2val_cur:
                    self._wrpy_pmid(prt, pmid, flds, fld2val_cur)
            prt.write("}\n\n") # End of pmid2info
            prt.write("# {COPYRIGHT}\n\n".format(COPYRIGHT=DL.get_copyright()))
            sys.stdout.write("  WROTE: {}\n".format(fout_py))

    def _wrpy_pmid(self, prt, pmid, flds, fld2val):
        """Write a PMID entry."""
        prt.write("  {PMID:>8} : {{\n".format(PMID=pmid))
        for fld_key in flds:
            fld_val = fld2val.get(fld_key, None)
            if fld_val is not None:
                #### prt.write("    {KEY} : ".format(KEY=addquot(fld_key)))
                prt.write("    {KEY} : ".format(KEY=''.join(["'", fld_key, "'"])))
                # Field: Date
                if fld_key in self.dates:
                    prt.write("{VAL}, # {C}\n".format(
                        VAL=repr(fld_val), C=fld_val.strftime("%Y %b %d")))
                # Field: TI, Abstract, etc.
                elif fld_key in self.join_these.keys():
                    self._wrpyfld_joined(prt, fld_val, pmid)
                # Field: list
                else:
                    prt.write("{VAL},\n".format(VAL=fld_val))
        prt.write("  },\n") # End of dictionary for one PMID

    @staticmethod
    def _get_fld2val_cur(fld2val_all, flds):
        """Get reduced set of fld2val."""
        fld2val_cur = {}
        for fld_key in flds:
            fld_val = fld2val_all.get(fld_key, None)
            if fld_val is not None:
                fld2val_cur[fld_key] = fld_val
        return fld2val_cur

    @staticmethod
    def _wrpy_get_sorted(pmid2info, flds):
        """Return pmid2info sorted by either date or by PubMed ID."""
        if 'DP' in flds:
            return sorted(pmid2info.items(), key=lambda t: t[1]['DP'], reverse=True)
        return sorted(pmid2info.items())

    @staticmethod
    def _wrpyfld_joined(prt, fld_val, pmid):
        """Write field into Python module."""
        #VAL_str = ''.join(['"', fld_val, '"'])
        if "'" in fld_val or '"' in fld_val:
            if '"""' not in fld_val:
                prt.write("{VAL},\n".format(VAL=''.join(['"""', fld_val, ' """'])))
            elif "'''" not in fld_val:
                prt.write("{VAL},\n".format(VAL=''.join(["'''", fld_val, " '''"])))
            else:
                raise Exception("QUOTE PROBLEM PMID({}): {}".format(pmid, fld_val))
        else:
            #### prt.write("{VAL},\n".format(VAL=addquot(fld_val)))
            prt.write("{VAL},\n".format(VAL=''.join(["'", fld_val, "'"])))

    date_patterns = [
        (r'(\d{4} \S{3} \d{1,2})\s*-', '%Y %b %d'),
        (r'(\d{4} \S{3})\w?\s*-', "%Y %b"),
        (r'(\d{4} \d{2})\s*-', "%Y %m"),
        (r'(\d{4} \w{3}) - \w{3}\b', '%Y %b'),
    ]

    # pylint: disable=too-many-statements
    def _init_date(self, fld2objs, fld, str_date, pmid):
        """Convert string date to datetime object."""
        # Compensate for fmts: 1993-1994, 2001 Jul 16-31, 2002 Sep 1-15, 2012 Sep-Oct
        # TBD: Use Python Template instead of multiple replace statements?
        # https://docs.python.org/3/library/string.html#template-strings
        # pylint: disable=bad-whitespace, too-many-branches
        str_date = str_date.replace("Autumn", "Oct")
        str_date = str_date.replace("Fall",   "Oct")
        str_date = str_date.replace("Winter", "Jan")
        str_date = str_date.replace("Spring", "Apr")
        str_date = str_date.replace("Summer", "Jun")
        str_date = str_date.replace("1st Quart", "Jan")
        str_date = str_date.replace("Apr.", "Apr")
        str_date = str_date.replace("November", "Nov")
        str_date = str_date.replace("December", "Dec")
        str_date = str_date.replace("/", "-")
        if "-" in str_date:
            # "2014 Jan-Feb" -> "2014 Feb"
            if len(str_date) == 12:
                str_date = str_date[0:8]
            else:
                # "2002 Sep 1-15" -> "2002 Sep 15"
                #### mtch = match(r'(\d{4} \w{3}) \d{1,2}-(\d{1,2})', str_date)
                mtch = match(r'(\d{4} \w{3}) \d{1,2}-', str_date)
                if mtch:
                    #### str_date = ' '.join([mtch.group(1), mtch.group(2)])
                    str_date = mtch.group(1)
                else:
                    # "1993-1994" -> "1994"
                    mtch = match(r'\d{4}-(\d{4})', str_date)
                    if mtch:
                        str_date = mtch.group(1)
                    else:
                        # 1983 Jul 28-Aug 3   ->   1983 Aug 3
                        #print "WAS", str_date
                        dateobj = self._matched(self.date_patterns, str_date)
                        ## if str_date == '1984 May 31-Jun 6':
                        ##     print('SSSSSSSSSSSSSSSSSSSSSSSSSSS({})'.format(str_date), dateobj)
                        if dateobj:
                            fld2objs[fld] = dateobj
                        else:
                            raise Exception("UNRECOGNIZED FORMAT({})".format(str_date))

                        #### mtch = match(r'(\d{4} \S{3} \d{1,2})\s*-', str_date)
                        #### if mtch:
                        ####     fld2objs[fld] = datetime.datetime.strptime(mtch.group(1), "%Y %b %d")
                        #### mtch = match(r'(\d{4} \S{3})\w?\s*-', str_date)
                        #### if mtch:
                        ####     fld2objs[fld] = datetime.datetime.strptime(mtch.group(1), "%Y %b")
                        #### # 2016 09-10  ->  2016 10
                        #### mtch = match(r'(\d{4} \d{2})\s*-', str_date)
                        #### if mtch:
                        ####     fld2objs[fld] = datetime.datetime.strptime(mtch.group(1), "%Y %m")
                        #### raise Exception("UNRECOGNIZED FORMAT({})".format(str_date))
        elif "/" in str_date:
            mtch = match(r'(\d{4} \w{3})/', str_date)
            if mtch:
                fld2objs[fld] = datetime.datetime.strptime(mtch.group(1), "%Y %b")
            raise Exception("UNRECOGNIZED FORMAT({})".format(str_date))
        else:
            # Apr 2017
            mtch = match(r'(\w{3} \d{4})', str_date)
            if mtch:
                fld2objs[fld] = datetime.datetime.strptime(mtch.group(1), "%b %Y")
        #print locale.getlocale()
        # fld2objs[fld] = datetime object
        date_str = self._lendate2fmt.get(len(str_date), None)
        if date_str is None:
            ## print("STRING DATE({})".format(str_date))
            mtch = search(r'(\d{4}) \d+th (\S+)', str_date) # "2016 20th Oct"
            if mtch:
                str_date = "{YEAR} {Mon}".format(YEAR=mtch.group(1), Mon=mtch.group(2))
                date_str = self._lendate2fmt.get(len(str_date), None)
        if date_str is None:
            raise Exception("BAD FORMAT ({})".format(str_date))
        fld2objs[fld] = datetime.datetime.strptime(str_date, date_str)

    @staticmethod
    def _matched(patterns, date_str):
        """Return True if any of the date-string matched any patterns"""
        for pattern, datefmt in patterns:
            mtch = match(pattern, date_str)
            if mtch:
                return datetime.datetime.strptime(mtch.group(1), datefmt)
        return None

# pylint: disable=too-few-public-methods
class ProcessLines:
    """Pre-process PubMed text lines, get a list of tuples of fields (TI) and values"""

    mhdangle = set(['herapy', 'on & control', 'ery', 'gy', 'peutic use'])

    def __init__(self, flds):
        self.flds = flds
        self.pmid = None
        self.fld = None
        self.fldvals = None

    def process_rawlines(self, ifstrm):
        """Read raw pubmed file, put all content that extends over one line into one line."""
        pmid2fldvals = {}
        self._reset_markers()
        for line in ifstrm:
            line = line.rstrip()
            if line: # If line is not empty
                self._extract_fldvals(line)
            elif self.pmid is not None: # blank line
                pmid2fldvals[self.pmid] = self.fldvals
                self._reset_markers()
        if self.pmid is not None: # blank line
            pmid2fldvals[self.pmid] = self.fldvals # Add last pmid to results
        return pmid2fldvals

    def _reset_markers(self):
        """Reset markers back to None"""
        self.pmid = None
        self.fld = None
        self.fldvals = None

    def _extract_fldvals(self, line):
        """Read and store ONE PMID record in fldvals"""
        # Start to read a new PMID record
        # Ex: PMID- 30101408
        if line[:6] == "PMID- ":
            self.pmid = int(line[6:])
            self.fldvals = [('PMID', [line[6:]])]
        # Continue reading a PMID record
        else:
            # Beginning of a field in the record
            line_body = line[6:]
            if line[4:5] == "-":
                self.fld = line[:4].rstrip()
                if self.fld in self.flds:
                    self.fldvals.append((self.fld, [line_body]))
            # Continuation of a fields in the record
            elif self.pmid is not None and self.fld is not None and self.fld in self.flds:
                # MH is not one text block. It is a list. Update the last item on the list. Example.
                #     MH  - Single-Chain Antibodies/administration &
                #           dosage/chemistry/*immunology/pharmacokinetics
                if self.fld == 'MH':
                    sep = " " if line_body not in self.mhdangle else ""
                    # self.fldvals indexes:
                    #     [-1] -> Last MH to be added
                    #      [0] -> 'MH'; [1] -> MH string
                    #     [-1] -> Last string in the last MH field
                    self.fldvals[-1][1][-1] = sep.join([self.fldvals[-1][1][-1], line_body])
                # Text is one block of text, like the Abstracts
                else:
                    self.fldvals[-1][1].append(line_body)


  # Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
