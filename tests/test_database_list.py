#!/usr/bin/env python3
"""Test retreiving the names of the Entrez databases"""

from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.base import EntrezUtilities

#pylint: disable=line-too-long
def test_database_list():
    """Test retreiving the names of the Entrez databases"""
    cfg = Cfg(check=False)
    eutils = EntrezUtilities(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
    dbs = sorted(eutils.get_database_list())
    assert len(dbs) > 30

    _run_one_db('pubmed', eutils)

    _run_einfo_db(dbs, eutils)
    _prt_einfo_db(dbs)


def _prt_einfo_db(dbs):
    """Print the list of databases"""
    assert dbs is not None, 'ERROR getting database list from NCBI E-Utils'
    print('\nNCBI NLM NIH Databases:')
    for idx, database in enumerate(dbs):
        print(f'  {idx:2}) {database}')

def _run_einfo_db(dbs, eutils):
    """Print summary for each database"""
    errs = []
    # idx         count database        last_update      menu_name                build                 description
    # ----------- ----- --------------- ---------------- ------------------------ --------------------- -----------
    #  0)    36,792,283 pubmed          2024/02/03 00:01 PubMed                   Build-2024.02.03.00.01 PubMed bibliographic record
    #  1) 1,258,364,124 protein         2024/01/31 07:36 Protein                  Build240129-0341m.1    Protein sequence record
    #  2)   618,784,579 nuccore         2024/02/01 10:13 Nucleotide               Build240130-0020m.1    Core Nucleotide db
    #  3)   676,903,368 ipg             2024/01/28 10:52 Identical Protein Groups Build240123-1018.1     Identical Protein Groups DB
    #  4)   618,784,579 nucleotide      2024/02/01 10:13 Nucleotide               Build240130-0020m.1    Core Nucleotide db
    #  5)       215,407 structure       2024/02/01 00:52 Structure                Build240131-2300.1     Three-dimensional molecular model
    #  6)        85,808 genome          2024/01/29 04:22 Genome                   Build240129-0155.1     Genomic sequences, contigs, and maps
    #  7)         1,962 annotinfo       2024/02/02 01:58 AnnotInfo                Build240202-0010.1     Annotinfo Database
    #  8)     2,185,490 assembly        2024/02/02 13:01 Assembly                 Build240202-0950.1     Genome Assembly Database
    #  9)       761,189 bioproject      2024/02/02 12:10 BioProject               Build240202-0625.1     BioProject Database
    # 10)    37,347,806 biosample       2024/02/02 17:35 BioSample                Build240202-1051m.1    BioSample Database
    # 11)    27,615,647 blastdbinfo     2024/02/02 02:12 BlastdbInfo              Build240201-1642.1     BlastdbInfo Database
    # 12)     1,179,114 books           2024/02/02 05:43 Books                    Build240202-0320.1     Books Database
    # 13)        64,234 cdd             2022/09/20 11:22 Conserved Domains        Build220919-0918.1     Conserved Domain Database
    # 14)     2,440,498 clinvar         2024/01/31 14:25 ClinVar                  Build240131-0840.1     ClinVar Database
    # 15)       363,717 gap             2023/05/22 04:11 dbGaP                    Build230522-0335m.1    dbGaP Data
    # 16)       136,796 gapplus         2017/09/29 04:56 GaPPlus                  Build170929-0435.1     Internal Genotypes and Phenotypes database
    # 17)     7,862,970 grasp           2015/01/26 16:10 grasp                    Build150126-1400.1     grasp Data
    # 18)     8,151,530 dbvar           2023/10/31 19:09 dbVar                    Build231031-1605.1     dbVar records
    # 19)    73,645,478 gene            2024/02/02 02:43 Gene                     Build240131-2245m.1    Gene database
    # 20)     7,254,747 gds             2024/02/02 02:36 GEO DataSets             Build240201-2002.1     GEO DataSets
    # 21)   128,414,055 geoprofiles     2024/01/30 05:06 GEO Profiles             Build160819-1300.323   Genes Expression Omnibus
    # 22)       222,213 medgen          2024/02/02 02:42 MedGen                   Build240202-0057.1     Medgen Database
    # 23)       354,830 mesh            2024/02/02 04:46 MeSH                     Build240202-0310.1     MeSH Database
    # 24)     1,645,193 nlmcatalog      2024/02/02 11:37 NLM Catalog              Build240202-0920.1     NLM Catalog Database
    # 25)        28,611 omim            2024/02/02 04:29 OMIM                     Build240202-0305.1     OMIM records
    # 26)         8,282 orgtrack        2024/02/02 12:30 Orgtrack                 Build240202-1030.1     Orgtrack Database
    # 27)     9,740,392 pmc             2024/02/02 12:46 PMC                      Build240202-0105m.1    PubMed Central
    # 28)       413,747 popset          2024/02/02 06:40 PopSet                   Build240202-0232m.1    PopSet sequence record
    # 29)     1,137,329 proteinclusters 2017/12/04 13:20 Protein Clusters         Build171204-1005.1     Protein Cluster record
    # 30)     1,627,721 pcassay         2024/02/02 12:30 PubChem BioAssay         Build240124-0940.1     PubChem BioAssay Database
    # 31)       169,843 protfam         2024/02/02 03:06 Protein Family Models    Build240201-2330.1     protfam DB
    # 32)   116,178,405 pccompound      2024/02/02 05:59 PubChem Compound         Build240201-0235m.1    PubChem Compound Database
    # 33)   311,214,073 pcsubstance     2024/02/01 20:41 PubChem Substance        Build240201-0235m.1    PubChem Substance Database
    # 34)       434,483 seqannot        2024/02/02 09:49 SeqAnnot                 Build240202-0729.1     SeqAnnot Database
    # 35) 1,121,739,543 snp             2022/11/22 11:07 SNP                      Build221118-1625.1     Single Nucleotide Polymorphisms
    # 36)    31,742,798 sra             2024/02/02 21:20 SRA                      Build240202-1208m.1    SRA Database
    # 37)     2,684,030 taxonomy        2024/02/02 11:51 Taxonomy                 Build240202-0815.1     Taxonomy db
    # 38)         8,497 biocollections  2023/12/06 04:35 Biocollections           Build231206-0315.1     Biocollections db
    # 39)        74,312 gtr             2024/02/02 12:28 GTR                      Build240202-1030.1     GTR Database

    dbkeys = {'dbname', 'menuname', 'description', 'dbbuild', 'count', 'lastupdate', 'fieldlist', 'linklist'}
    print('\n')
    print('Idx Num. of Items Database        Last update      Menu name                Build                  Description')
    print('--  ------------- --------------- ---------------- ------------------------ ---------------------- -----------')
    for idx, database in enumerate(dbs):
        try:
            rsp = eutils.run_eutilscmd('einfo', db=database, retmode='json')
        except RuntimeError as errobj:
            msg = (f'**FATAL: {str(errobj)}\n'
                   f'**FATAL: UNSUCCESSFUL GET FROM NCBI E-Utils `einfo` for database({database})\n')
            print(msg)
            errs.append(msg)
            rsp = None

        if rsp:
            assert 'einforesult' in rsp, f'NO EINFORESULT IN RESPONSE: {rsp}'
            assert 'dbinfo' in rsp['einforesult'], f'NO DBINFO IN EINFORESULT RESPONSE: {rsp}'
            dbinfo = rsp['einforesult']['dbinfo']
            assert len(dbinfo) == 1, dbinfo
            dbinfo = dbinfo[0]
            assert dbinfo.keys() == dbkeys, set(dbinfo.keys()).difference(dbkeys)
            dbinfo['count'] = int(dbinfo['count'])
            print(f'{idx:2}) '
                  f'{dbinfo["count"]:13,} '
                  f'{database:15} '
                  f'{dbinfo["lastupdate"]} '
                  f'{dbinfo["menuname"]:24} '
                  f'{dbinfo["dbbuild"]:22} '
                  f'{dbinfo["description"]} '
            )
    assert len(errs) <= 0, f'{len(errs)} ERRORS FOUND:\n' + '\n'.join(errs)


def _run_one_db(database, eutils):
    """Get details for only one database"""
    print(f'GETTING einfo ON {database}')
    rsp = eutils.run_eutilscmd('einfo', db=database, retmode='json')
    assert rsp, f'NO RESPONSE: {rsp}'
    assert 'einforesult' in rsp, f'NO EINFORESULT IN RESPONSE: {rsp}'
    assert 'dbinfo' in rsp['einforesult'], f'NO DBINFO IN EINFORESULT RESPONSE: {rsp}'
    dbinfo = rsp['einforesult']['dbinfo']
    for elem in dbinfo:
        for key, val in elem.items():
            print('')
            if key in {'fieldlist', 'linklist'}:
                for item in val:
                    print(f'{database} {key:12} {item}')
            else:
                print(f'{database} {key:12} {val}')


if __name__ == '__main__':
    test_database_list()
