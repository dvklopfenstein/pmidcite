# Sorting
https://unix.stackexchange.com/questions/104525/sort-based-on-the-third-column

## Sorting by citation count, then by date
```
grep PubMed pmidcite.txt | sort -k 6,6 -k 2,2 -r
```

### A note about the second number
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

### Add all cited_by numbers for an author
```
$ grep TOP pmidcite_Santangelo_GM.txt | sort -k 2,2 -k 6,6 -r | awk '{s+=$6} END {print s}'
```
