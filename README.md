# PMID Cite
Traverse [**NIH iCite**](https://icite.od.nih.gov/) citations and references and download 
[**PubMed**](https://pubmed.ncbi.nlm.nih.gov/) summaries from the command line.

## How about Google Search?
Google Scholar was found to be inappropriate as principal search system [1][2] for peer-reviewed research papers due to:
 * The same query can produce different results at different times
 * Poor boolean search interface:
    * Not documented
    * A space ' ' is used to represent the logical AND
    * Nesting of subexpressions limited to one level
    * No history function
    * No clear access to booleans using Google's search expression builder
 * Queries are truncated to 256 characters without warning
    * Which may result in an increased number of false positive results
 * There are a maximum of 1000 results:
   * Displayed in steps of 20 per page.
   * Undocumented sort of full results, when not sorted by date
 * Unknown size of database
 * Crawler-based search engines function differently than bibliographic databases which have a curated entries

## Emails

  * [**2019_1204 PubMed cited_by list**]()

### PubMed query fir cited_by

‐‐‐‐‐‐‐ Original Message ‐‐‐‐‐‐‐
On Wednesday, December 4, 2019 8:22 AM, NLM Support <nlm-support@nlm.nih.gov> wrote:



Dear D.V. Klopfenstein:

The U. S. National Library of Medicine (NLM) received your message about whether there is a PubMed query that can  retrieve all the PMIDs on the cited_by list for one paper's PMID

Please note that MEDLINE/PubMed does not indicate the number of times an article, author, or journal is cited or provide journal impact factor information.

The PubMed abstract may include a Cited in PubMed Central (PMC) articles portlet for
PubMed citations cited by PMC articles.

The Cited in PMC portlet lists the articles in PubMed Central for the cited PubMed citation.
(For example, see PMID: 28750494 at https://www.ncbi.nlm.nih.gov/pubmed/?term=28750494 )


Check with a librarian at your local medical or university library for help locating non-NLM
resources that have citation and impact factor information such as
Google Scholar, SCOPUS, ISI Web of Knowledge® (Web of Science, Science Citation Index, Social Science Citation Index) and Journal Citation Reports.

We hope you find this information helpful.

Leonore W. Burts, MSLIS
Customer Service Librarian
Contractor for the National Library of Medicine, NIH
8600 Rockville Pike
Bethesda, MD 20894 31655
https://support.nlm.nih.gov

****
* PLEASE DO NOT MODIFY THE SUBJECT LINE OF THIS EMAIL WHEN RESPONDING TO ENSURE CORRECT TRACKING *


Case Information:
Case #: CAS-459606-W7K5F9
Customer Name: DV Klopfenstein
Customer Email: dvklopfenstein@protonmail.com
Case Created: 2019-12-03T19:28:14Z


Summary: PubMed Query to find the cited_by list for a specific PMID?


Details: Hello,


Thank you for your great PubMed tools. They are extremely useful.
Is there a PubMed query that I can use to find all the PMIDs on the cited_by list for one paper's PMID?
If this query is possible, how to modify it to return a list of PMIDs in the reference list for a specific paper?

Thank you for your time


## Sorting
https://unix.stackexchange.com/questions/104525/sort-based-on-the-third-column

### Sorting by citation count, then by date
```
grep PubMed pmidcite.txt | sort -k 6,6 -k 2,2 -r
```

#### A note about the second number
You must use 6,6 and 2,2, rather than 6 and 2.
'sort -k 6' searches from 6 until the end of the line.

So these sorts are not the same, but are similar.
The first sorts by cite_by_cnt(6),
then by year(2), then by PMID and the rest of the line.
```
$ grep TOP pmidcite.txt | sort -k 6 -k 2
$ grep TOP pmidcite.txt | sort -k 6,6 -k 2,2
```

But 'sort by year, then citation' yield much different results
because it first sorts by year, then PMID, and the rest of the line
before sorting for citation count.
```
$ grep PubMed pmidcite_litsrch.txt | sort -k 2,2 -k 6,6 -r
$ grep PubMed pmidcite_litsrch.txt | sort -k 2 -k 6 -r
```

## Links to other PubMed tools

* [PubMed parser](https://github.com/titipata/pubmed_parser)
* [pymed](https://github.com/gijswobben/pymed)    
* [paper2remarkable](https://github.com/GjjvdBurg/paper2remarkable)
* [pubmed-lookup](https://github.com/mfcovington/pubmed-lookup)

Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
