#!/usr/bin/env python3
"""Test retreiving the names of the Entrez databases"""

import sys
from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.base import EntrezUtilities

#pylint: disable=line-too-long
def test_database_list(einfo_each_db=False):
    """Test retreiving the names of the Entrez databases"""
    cfg = Cfg()
    eutils = EntrezUtilities(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
    dbs = eutils.get_database_list()

    if einfo_each_db:
        dbkeys = {'dbname', 'menuname', 'description', 'dbbuild', 'count', 'lastupdate', 'fieldlist', 'linklist'}
        fmt = '{I:>2}) {lastupdate} {count:12,} {dbname:15} {menuname:24} {dbbuild:20} {description}'
        _run_einfo_db(dbs, fmt, dbkeys, eutils)
    else:
        _prt_einfo_db(dbs)
    assert len(dbs) > 30

    _run_one_db('pubmed', eutils)

def _prt_einfo_db(dbs):
    """Print the list of databases"""
    for idx, database in enumerate(dbs):
        print('  {I}) {DB}'.format(I=idx, DB=database))

def _run_einfo_db(dbs, fmt, dbkeys, eutils):
    """Print summary for each database"""
    #  0) 2019/11/24 07:24   30,365,981 pubmed          PubMed                   Build191123-2212m.2  PubMed bibliographic record
    #  1) 2019/11/23 01:06  806,297,069 protein         Protein                  Build191121-0946m.1  Protein sequence record
    #  2) 2019/11/23 10:05  413,490,832 nuccore         Nucleotide               Build191121-2215m.1  Core Nucleotide db
    #  3) 2019/11/24 10:51  259,375,691 ipg             Identical Protein Groups Build191122-1628.1   Identical Protein Groups DB
    #  4) 2019/11/23 10:05  413,490,832 nuccore         Nucleotide               Build191121-2215m.1  Core Nucleotide db
    #  5) 2019/11/24 15:08      157,258 structure       Structure                Build191124-1400.1   Three-dimensional molecular model
    #  6) 2019/11/24 02:48      174,147 sparcle         Sparcle                  Build191124-0200.1   Protein classification by domain architecture
    #  7) 2019/11/24 10:08       61,115 genome          Genome                   Build191124-0910.1   Genomic sequences, contigs, and maps
    #  8) 2019/11/24 01:26        1,004 annotinfo       AnnotInfo                Build191124-0035.1   Annotinfo Database
    #  9) 2019/11/24 08:21      563,861 assembly        Assembly                 Build191124-0630.1   Genome Assembly Database
    # 10) 2019/11/24 08:07      397,797 bioproject      BioProject               Build191124-0630.1   BioProject Database
    # 11) 2019/11/24 10:08   12,081,118 biosample       BioSample                Build191124-0732.1   BioSample Database
    # 12) 2019/11/24 03:18    6,848,222 blastdbinfo     BlastdbInfo              Build191124-0237.1   BlastdbInfo Database
    # 13) 2019/11/24 03:13      880,423 books           Books                    Build191124-0220.1   Books Database
    # 14) 2019/04/05 20:21       57,242 cdd             Conserved Domains        Build190405-1636.1   Conserved Domain Database
    # 15) 2019/11/19 13:51      568,903 clinvar         ClinVar                  Build191118-1740.1   ClinVar Database
    # 16) 2019/11/21 13:23      362,870 gap             dbGaP                    Build191121-1305m.1  dbGaP Data
    # 17) 2017/09/29 04:56      136,796 gapplus         GaPPlus                  Build170929-0435.1   Internal Genotypes and Phenotypes database
    # 18) 2015/01/26 16:10    7,862,970 grasp           grasp                    Build150126-1400.1   grasp Data
    # 19) 2019/11/21 15:09    5,930,429 dbvar           dbVar                    Build191121-1215.1   dbVar records
    # 20) 2019/11/22 08:28   37,594,398 gene            Gene                     Build191121-2245m.1  Gene database
    # 21) 2019/11/23 17:24    3,451,245 gds             GEO DataSets             Build191123-1612.1   GEO DataSets
    # 22) 2019/11/19 03:58  128,414,055 geoprofiles     GEO Profiles             Build160819-1300.170 Genes Expression Omnibus
    # 23) 2015/03/12 16:41      141,268 homologene      HomoloGene               Build140512-1105.2   HomoloGene Database
    # 24) 2019/11/24 07:17      327,018 medgen          MedGen                   Build191124-0647.1   Medgen Database
    # 25) 2019/11/24 03:33      279,004 mesh            MeSH                     Build191124-0310.1   MeSH Database
    # 26) 2017/10/02 15:00        3,941 ncbisearch      NCBI Web Site            Build171002-1425.1   NcbiSearch Database
    # 27) 2019/11/24 07:06    1,609,391 nlmcatalog      NLM Catalog              Build191124-0625.1   NLM Catalog Database
    # 28) 2019/11/24 03:31       26,515 omim            OMIM                     Build191124-0305.1   OMIM records
    # 29) 2019/11/24 03:46        6,669 orgtrack        Orgtrack                 Build191124-0315.1   Orgtrack Database
    # 30) 2019/11/22 07:25    5,932,780 pmc             PMC                      Build191122-0110m.1  PubMed Central
    # 31) 2019/11/24 02:23      335,384 popset          PopSet                   Build191123-2357m.1  PopSet sequence record
    # 32) 2019/09/27 10:50   32,407,923 probe           Probe                    Build190927-0809.1   Probe DB
    # 33) 2017/12/04 13:20    1,137,329 proteinclusters Protein Clusters         Build171204-1005.1   Protein Cluster record
    # 34) 2019/11/20 13:18    1,067,675 pcassay         PubChem BioAssay         Build191120-1114.1   PubChem BioAssay Database
    # 35) 2019/02/27 14:39      983,968 biosystems      BioSystems               Build170421-2146.2   BioSystems Database
    # 36) 2019/11/24 03:55   96,889,200 pccompound      PubChem Compound         Build191123-1255m.1  PubChem Compound Database
    # 37) 2019/11/23 22:52  246,749,114 pcsubstance     PubChem Substance        Build191123-1255m.1  PubChem Substance Database
    # 38) 2019/11/24 16:16      227,109 seqannot        SeqAnnot                 Build191124-1459.1   SeqAnnot Database
    # 39) 2019/10/28 15:20  686,600,501 snp             SNP                      Build191026-1755.1   Single Nucleotide Polymorphisms
    # 40) 2019/11/21 13:02    9,410,725 sra             SRA                      Build191118-1648m.1  SRA Database
    # 41) 2019/11/24 15:15    2,305,371 taxonomy        Taxonomy                 Build191124-1420.1   Taxonomy db
    # 42) 2019/11/24 03:39        8,099 biocollections  Biocollections           Build191124-0315.1   Biocollections db
    # 43) 2019/11/24 04:22       60,056 gtr             GTR                      Build191124-0315.1   GTR Database
    for idx, database in enumerate(dbs):
        dct = eutils.run_eutilscmd('einfo', db=database, retmode='json')
        dct['count'] = int(dct['count'])
        assert set(dct.keys()) == dbkeys
        # fieldlist linklist
        print(fmt.format(I=idx, **dct))

def _run_one_db(database, eutils):
    """Get details for only one database"""
    # fieldlist {'name': 'ALL', 'fullname': 'All Fields', 'description': 'All terms from all searchable fields', 'termcount': '229621543', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'UID', 'fullname': 'UID', 'description': 'Unique number assigned to publication', 'termcount': '0', 'isdate': 'N', 'isnumerical': 'Y', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'FILT', 'fullname': 'Filter', 'description': 'Limits the records', 'termcount': '5595', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'TITL', 'fullname': 'Title', 'description': 'Words in title of publication', 'termcount': '17530080', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'WORD', 'fullname': 'Text Word', 'description': 'Free text associated with publication', 'termcount': '64363736', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'MESH', 'fullname': 'MeSH Terms', 'description': 'Medical Subject Headings assigned to publication', 'termcount': '611145', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'Y', 'ishidden': 'N'}
    # fieldlist {'name': 'MAJR', 'fullname': 'MeSH Major Topic', 'description': 'MeSH terms of major importance to publication', 'termcount': '549650', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'Y', 'ishidden': 'N'}
    # fieldlist {'name': 'AUTH', 'fullname': 'Author', 'description': 'Author(s) of publication', 'termcount': '20370825', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'JOUR', 'fullname': 'Journal', 'description': 'Journal abbreviation of publication', 'termcount': '202064', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'AFFL', 'fullname': 'Affiliation', 'description': "Author's institutional affiliation and address", 'termcount': '53290063', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'ECNO', 'fullname': 'EC/RN Number', 'description': 'EC number for enzyme or CAS registry number', 'termcount': '104839', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'SUBS', 'fullname': 'Supplementary Concept', 'description': 'CAS chemical name or MEDLINE Substance Name', 'termcount': '260302', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PDAT', 'fullname': 'Date - Publication', 'description': 'Date of publication', 'termcount': '40498', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'EDAT', 'fullname': 'Date - Entrez', 'description': 'Date publication first accessible through Entrez', 'termcount': '39450', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'VOL', 'fullname': 'Volume', 'description': 'Volume number of publication', 'termcount': '13565', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PAGE', 'fullname': 'Pagination', 'description': 'Page number(s) of publication', 'termcount': '3706212', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PTYP', 'fullname': 'Publication Type', 'description': 'Type of publication (e.g., review)', 'termcount': '87', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'Y', 'ishidden': 'N'}
    # fieldlist {'name': 'LANG', 'fullname': 'Language', 'description': 'Language of publication', 'termcount': '59', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'ISS', 'fullname': 'Issue', 'description': 'Issue number of publication', 'termcount': '16844', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'SUBH', 'fullname': 'MeSH Subheading', 'description': 'Additional specificity for MeSH term', 'termcount': '76', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'Y', 'ishidden': 'N'}
    # fieldlist {'name': 'SI', 'fullname': 'Secondary Source ID', 'description': 'Cross-reference from publication to other databases', 'termcount': '7803945', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'MHDA', 'fullname': 'Date - MeSH', 'description': 'Date publication was indexed with MeSH terms', 'termcount': '39307', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'TIAB', 'fullname': 'Title/Abstract', 'description': 'Free text associated with Abstract/Title', 'termcount': '53950093', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'OTRM', 'fullname': 'Other Term', 'description': 'Other terms associated with publication', 'termcount': '4333544', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'INVR', 'fullname': 'Investigator', 'description': 'Investigator', 'termcount': '1751589', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'COLN', 'fullname': 'Author - Corporate', 'description': 'Corporate Author of publication', 'termcount': '263413', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'CNTY', 'fullname': 'Place of Publication', 'description': 'Country of publication', 'termcount': '229', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'PAPX', 'fullname': 'Pharmacological Action', 'description': 'MeSH pharmacological action pre-explosions', 'termcount': '541', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'GRNT', 'fullname': 'Grant Number', 'description': 'NIH Grant Numbers', 'termcount': '4813499', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'MDAT', 'fullname': 'Date - Modification', 'description': 'Date of last modification', 'termcount': '7122', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'CDAT', 'fullname': 'Date - Completion', 'description': 'Date of completion', 'termcount': '11914', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PID', 'fullname': 'Publisher ID', 'description': 'Publisher ID', 'termcount': '31710212', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'FAUT', 'fullname': 'Author - First', 'description': 'First Author of publication', 'termcount': '10869725', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'FULL', 'fullname': 'Author - Full', 'description': 'Full Author Name(s) of publication', 'termcount': '13967806', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'FINV', 'fullname': 'Investigator - Full', 'description': 'Full name of investigator', 'termcount': '1019252', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'TT', 'fullname': 'Transliterated Title', 'description': 'Words in transliterated title of publication', 'termcount': '2335289', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'LAUT', 'fullname': 'Author - Last', 'description': 'Last Author of publication', 'termcount': '9077623', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PPDT', 'fullname': 'Print Publication Date', 'description': 'Date of print publication', 'termcount': '40489', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'EPDT', 'fullname': 'Electronic Publication Date', 'description': 'Date of Electronic publication', 'termcount': '7738', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'LID', 'fullname': 'Location ID', 'description': 'ELocation ID', 'termcount': '23257968', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'CRDT', 'fullname': 'Date - Create', 'description': 'Date publication first accessible through Entrez', 'termcount': '30655', 'isdate': 'Y', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'BOOK', 'fullname': 'Book', 'description': 'ID of the book that contains the document', 'termcount': '6644', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'ED', 'fullname': 'Editor', 'description': "Section's Editor", 'termcount': '5327', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'ISBN', 'fullname': 'ISBN', 'description': 'ISBN', 'termcount': '3983', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PUBN', 'fullname': 'Publisher', 'description': "Publisher's name", 'termcount': '605', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'AUCL', 'fullname': 'Author Cluster ID', 'description': 'Author Cluster ID', 'termcount': '0', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'EID', 'fullname': 'Extended PMID', 'description': 'Extended PMID', 'termcount': '30344250', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'DSO', 'fullname': 'DSO', 'description': 'Additional text from the summary', 'termcount': '399499', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'Y'}
    # fieldlist {'name': 'AUID', 'fullname': 'Author - Identifier', 'description': 'Author Identifier', 'termcount': '4453916', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'PS', 'fullname': 'Subject - Personal Name', 'description': 'Personal Name as Subject', 'termcount': '550254', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'Y', 'hierarchy': 'N', 'ishidden': 'N'}
    # fieldlist {'name': 'COIS', 'fullname': 'Conflict of Interest Statements', 'description': 'Conflict of Interest Statements', 'termcount': '255718', 'isdate': 'N', 'isnumerical': 'N', 'singletoken': 'N', 'hierarchy': 'N', 'ishidden': 'N'}
    # linklist {'name': 'pubmed_assembly', 'menu': 'Assembly', 'description': 'Assembly', 'dbto': 'assembly'}
    # linklist {'name': 'pubmed_bioproject', 'menu': 'Project Links', 'description': 'Related Projects', 'dbto': 'bioproject'}
    # linklist {'name': 'pubmed_biosample', 'menu': 'BioSample Links', 'description': 'BioSample links', 'dbto': 'biosample'}
    # linklist {'name': 'pubmed_biosystems', 'menu': 'BioSystem Links', 'description': 'BioSystems', 'dbto': 'biosystems'}
    # linklist {'name': 'pubmed_books_refs', 'menu': 'Cited in Books', 'description': 'PubMed links associated with Books', 'dbto': 'books'}
    # linklist {'name': 'pubmed_cdd', 'menu': 'Conserved Domain Links', 'description': 'Link to related CDD entry', 'dbto': 'cdd'}
    # linklist {'name': 'pubmed_clinvar', 'menu': 'ClinVar', 'description': 'Clinical variations associated with publication', 'dbto': 'clinvar'}
    # linklist {'name': 'pubmed_clinvar_calculated', 'menu': 'ClinVar (calculated)', 'description': 'Clinical variations calculated to be associated with publication', 'dbto': 'clinvar'}
    # linklist {'name': 'pubmed_dbvar', 'menu': 'dbVar', 'description': 'Link from PubMed to dbVar', 'dbto': 'dbvar'}
    # linklist {'name': 'pubmed_gap', 'menu': 'dbGaP Links', 'description': 'Related dbGaP record', 'dbto': 'gap'}
    # linklist {'name': 'pubmed_gds', 'menu': 'GEO DataSet Links', 'description': 'Related GEO DataSets', 'dbto': 'gds'}
    # linklist {'name': 'pubmed_gene', 'menu': 'Gene Links', 'description': 'Link to related Genes', 'dbto': 'gene'}
    # linklist {'name': 'pubmed_gene_bookrecords', 'menu': 'Gene (from Bookshelf)', 'description': 'Gene records in this citation', 'dbto': 'gene'}
    # linklist {'name': 'pubmed_gene_citedinomim', 'menu': 'Gene (OMIM) Links', 'description': 'PubMed links to Gene derived from pubmed_omim_cited links', 'dbto': 'gene'}
    # linklist {'name': 'pubmed_gene_pmc_nucleotide', 'menu': 'Gene (nucleotide/PMC)', 'description': 'Records in Gene identified from shared sequence and PMC links.', 'dbto': 'gene'}
    # linklist {'name': 'pubmed_gene_rif', 'menu': 'Gene (GeneRIF) Links', 'description': 'Link to Gene for the GeneRIF subcategory', 'dbto': 'gene'}
    # linklist {'name': 'pubmed_genome', 'menu': 'Genome Links', 'description': 'Published genome sequences', 'dbto': 'genome'}
    # linklist {'name': 'pubmed_geoprofiles', 'menu': 'GEO Profile Links', 'description': 'GEO records associated with pubmed record', 'dbto': 'geoprofiles'}
    # linklist {'name': 'pubmed_homologene', 'menu': 'HomoloGene Links', 'description': 'Related HomoloGene', 'dbto': 'homologene'}
    # linklist {'name': 'pubmed_medgen', 'menu': 'MedGen', 'description': 'Related information in MedGen', 'dbto': 'medgen'}
    # linklist {'name': 'pubmed_medgen_bookshelf_cited', 'menu': 'MedGen (Bookshelf cited)', 'description': 'Related records in MedGen based on citations in GeneReviews and Medical Genetics Summaries', 'dbto': 'medgen'}
    # linklist {'name': 'pubmed_medgen_genereviews', 'menu': 'MedGen (GeneReviews)', 'description': 'Related MedGen records', 'dbto': 'medgen'}
    # linklist {'name': 'pubmed_medgen_omim', 'menu': 'MedGen (OMIM)', 'description': 'Related information in MedGen (OMIM)', 'dbto': 'medgen'}
    # linklist {'name': 'pubmed_nuccore', 'menu': 'Nucleotide Links', 'description': 'Published Nucleotide sequences', 'dbto': 'nuccore'}
    # linklist {'name': 'pubmed_nuccore_refseq', 'menu': 'Nucleotide (RefSeq) Links', 'description': 'Link to Nucleotide RefSeqs', 'dbto': 'nuccore'}
    # linklist {'name': 'pubmed_nuccore_weighted', 'menu': 'Nucleotide (Weighted) Links', 'description': 'Links to nuccore', 'dbto': 'nuccore'}
    # linklist {'name': 'pubmed_omim_bookrecords', 'menu': 'OMIM (from Bookshelf)', 'description': 'OMIM records in this citation', 'dbto': 'omim'}
    # linklist {'name': 'pubmed_omim_calculated', 'menu': 'OMIM (calculated) Links', 'description': 'OMIM (calculated) Links', 'dbto': 'omim'}
    # linklist {'name': 'pubmed_omim_cited', 'menu': 'OMIM (cited) Links', 'description': 'OMIM (cited) Links', 'dbto': 'omim'}
    # linklist {'name': 'pubmed_pcassay', 'menu': 'PubChem BioAssay', 'description': 'Related PubChem BioAssay', 'dbto': 'pcassay'}
    # linklist {'name': 'pubmed_pccompound', 'menu': 'PubChem Compound', 'description': 'Related PubChem Compound', 'dbto': 'pccompound'}
    # linklist {'name': 'pubmed_pccompound_mesh', 'menu': 'PubChem Compound (MeSH Keyword)', 'description': 'Related PubChem Compound via MeSH', 'dbto': 'pccompound'}
    # linklist {'name': 'pubmed_pccompound_publisher', 'menu': 'PubChem Compound (Publisher)', 'description': 'Publisher deposited structures linked to PubChem Compound', 'dbto': 'pccompound'}
    # linklist {'name': 'pubmed_pcsubstance', 'menu': 'PubChem Substance Links', 'description': 'Related PubChem Substance', 'dbto': 'pcsubstance'}
    # linklist {'name': 'pubmed_pcsubstance_bookrecords', 'menu': 'PubChem Substance (from Bookshelf)', 'description': 'Structures in the PubChem Substance database in this citation', 'dbto': 'pcsubstance'}
    # linklist {'name': 'pubmed_pcsubstance_publisher', 'menu': 'PubChem Substance (Publisher)', 'description': 'PubChem Substances supplied by publisher', 'dbto': 'pcsubstance'}
    # linklist {'name': 'pubmed_pmc', 'menu': 'PMC Links', 'description': 'Free full text articles in PMC', 'dbto': 'pmc'}
    # linklist {'name': 'pubmed_pmc_bookrecords', 'menu': 'References in PMC for this Bookshelf citation', 'description': 'Full text of articles in PubMed Central cited in this record', 'dbto': 'pmc'}
    # linklist {'name': 'pubmed_pmc_embargo', 'menu': '', 'description': 'Embargoed PMC article associated with PubMed', 'dbto': 'pmc'}
    # linklist {'name': 'pubmed_pmc_local', 'menu': '', 'description': 'Free full text articles in PMC', 'dbto': 'pmc'}
    # linklist {'name': 'pubmed_pmc_refs', 'menu': 'Cited in PMC', 'description': 'PubMed links associated with PMC', 'dbto': 'pmc'}
    # linklist {'name': 'pubmed_popset', 'menu': 'PopSet Links', 'description': 'Published population set', 'dbto': 'popset'}
    # linklist {'name': 'pubmed_probe', 'menu': 'Probe Links', 'description': 'Related Probe entry', 'dbto': 'probe'}
    # linklist {'name': 'pubmed_protein', 'menu': 'Protein Links', 'description': 'Published protein sequences', 'dbto': 'protein'}
    # linklist {'name': 'pubmed_protein_refseq', 'menu': 'Protein (RefSeq) Links', 'description': 'Link to Protein RefSeqs', 'dbto': 'protein'}
    # linklist {'name': 'pubmed_protein_weighted', 'menu': 'Protein (Weighted) Links', 'description': 'Links to protein', 'dbto': 'protein'}
    # linklist {'name': 'pubmed_proteinclusters', 'menu': 'Protein Cluster Links', 'description': 'Related Protein Clusters', 'dbto': 'proteinclusters'}
    # linklist {'name': 'pubmed_pubmed', 'menu': 'Similar articles', 'description': 'Similar PubMed articles, obtained by matching text and MeSH terms', 'dbto': 'pubmed'}
    # linklist {'name': 'pubmed_pubmed_alsoviewed', 'menu': 'Articles frequently viewed together', 'description': 'Articles frequently viewed together', 'dbto': 'pubmed'}
    # linklist {'name': 'pubmed_pubmed_bookrecords', 'menu': 'References for this Bookshelf citation', 'description': 'PubMed abstracts for articles cited in this record', 'dbto': 'pubmed'}
    # linklist {'name': 'pubmed_pubmed_refs', 'menu': 'References for PMC Articles', 'description': 'References for this PMC Article', 'dbto': 'pubmed'}
    # linklist {'name': 'pubmed_snp', 'menu': 'SNP Links', 'description': 'PubMed to SNP links', 'dbto': 'snp'}
    # linklist {'name': 'pubmed_snp_cited', 'menu': 'SNP (Cited)', 'description': 'Related SNP (Cited) records', 'dbto': 'snp'}
    # linklist {'name': 'pubmed_sra', 'menu': 'SRA Links', 'description': 'Links to Short Read Archive Experiments', 'dbto': 'sra'}
    # linklist {'name': 'pubmed_structure', 'menu': 'Structure Links', 'description': 'Published 3D structures', 'dbto': 'structure'}
    # linklist {'name': 'pubmed_taxonomy_entrez', 'menu': 'Taxonomy via GenBank', 'description': 'Related Taxonomy entry computed using other Entrez links', 'dbto': 'taxonomy'}
    # linklist {'name': 'pubmed_unigene', 'menu': 'UniGene Links', 'description': 'Related UniGene', 'dbto': 'unigene'}
    dct = eutils.run_eutilscmd('einfo', db=database, retmode='json')
    for item in dct['fieldlist']:
        print('fieldlist', item)
    for item in dct['linklist']:
        print('linklist', item)
    print(dct.keys())


if __name__ == '__main__':
    test_database_list(len(sys.argv) != 1)
