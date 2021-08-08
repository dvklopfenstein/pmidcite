#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""For installing pmidcite package and accompanying scripts."""

from os.path import abspath
from os.path import dirname
from os.path import join
# from distutils.core import setup
from glob import glob
from pathlib import PurePosixPath
from setuptools import setup
# import versioneer


NAME = 'pmidcite'

PACKAGES = [
    'pmidcite',
    'pmidcite.cli',
    'pmidcite.eutils',
    'pmidcite.eutils.cmds',
    'pmidcite.eutils.pubmed',
    'pmidcite.eutils.pubmed.counts',
    'pmidcite.eutils.pubmed.mesh',
    'pmidcite.icite',
    'pmidcite.plot',
]

PACKAGE_DIRS = {p:join('src', PurePosixPath(*p.split('.'))) for p in PACKAGES}

def get_long_description():
    """Return the contents of the README.md as a string"""
    dir_cur = abspath(dirname(__file__))
    with open(join(dir_cur, 'README.md'), encoding='utf-8') as ifstrm:
        return ifstrm.read()


setup(
    name=NAME,
    ## version=versioneer.get_version(),
    version='0.0.14',
    author='DV Klopfenstein',
    author_email='dvklopfenstein@protonmail.com',
    ## cmdclass=versioneer.get_cmdclass(),
    packages=PACKAGES,
    package_dir=PACKAGE_DIRS,
    # https://stackoverflow.com/questions/18787036/difference-between-entry-points-console-scripts-and-scripts-in-setup-py
    scripts=glob('src/bin/*.py'),
    # https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    url='http://github.com/dvklopfenstein/pmidcite',
    description="Augment's a PubMed literature search with citation data from NIH-OCC's iCite.",
    # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    # install_requires=['docopt'],
)
