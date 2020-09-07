#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""For installing pmidcite package and accompanying scripts."""

from os.path import abspath
from os.path import dirname
from os.path import join
from distutils.core import setup
import versioneer
from glob import glob

def get_long_description():
    """Return the contents of the README.md as a string"""
    dir_cur = abspath(dirname(__file__))
    with open(join(dir_cur, 'README.md'), encoding='utf-8') as ifstrm:
        return ifstrm.read()


setup(
    name='pmidcite',
    version=versioneer.get_version(),
    author='DV Klopfenstein',
    author_email='dvklopfenstein@protonmail.com',
    # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    cmdclass=versioneer.get_cmdclass(),
    packages=[
        'pmidcite',
        'pmidcite.cli',
        'pmidcite.eutils',
        'pmidcite.eutils.cmds',
        'pmidcite.eutils.pubmed',
        'pmidcite.eutils.pubmed.counts',
        'pmidcite.eutils.pubmed.mesh',
        'pmidcite.icite',
        'pmidcite.plot',
    ],
    package_dir={
        'pmidcite': 'src/pmidcite',
        'pmidcite.cli': 'src/pmidcite/cli',
        'pmidcite.eutils': 'src/pmidcite/eutils',
        'pmidcite.eutils.cmds': 'src/pmidcite/eutils/cmds',
        'pmidcite.eutils.pubmed': 'src/pmidcite/eutils/pubmed',
        'pmidcite.eutils.pubmed.counts': 'src/pmidcite/eutils/pubmed/counts',
        'pmidcite.eutils.pubmed.mesh': 'src/pmidcite/eutils/pubmed/mesh',
        'pmidcite.icite': 'src/pmidcite/icite',
        'pmidcite.plot': 'src/pmidcite/plot',
    },
    scripts=glob('src/bin/*.py'),
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Version Control :: Git',
    ],
    url='http://github.com/dvklopfenstein/pmidcite',
    description="Augment's a PubMed literature search with citation data from NIH's iCite.",
    # install_requires=['docopt'],
)
