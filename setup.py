#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""For installing pmidcite package and accompanying scripts."""

from os.path import abspath
from os.path import dirname
from os.path import join
# from distutils.core import setup
from glob import glob
from setuptools import setup
# import versioneer

__copyright__ = 'Copyright (C) 2019, DV Klopfenstein, PhD. All rights reserved'
__author__ = 'DV Klopfenstein, PhD'

NAME = 'pmidcite'

PACKAGES = [
    'pmidcite',
    'pmidcite.cli',
    'pmidcite.eutils',
    'pmidcite.eutils.cmds',
    'pmidcite.eutils.pubmed',
    'pmidcite.eutils.pubmed.counts',
    'pmidcite.icite',
    'pmidcite.icite.dnldr',
    'pmidcite.scripts',
    'pmidcite.plot',
]

PACKAGE_DIRS = {p:join('src', *p.split('.')) for p in PACKAGES}


def get_long_description():
    """Return the contents of the README.md as a string"""
    dir_cur = abspath(dirname(__file__))
    # python3
    #with open(join(dir_cur, 'README.md'), encoding='utf-8') as ifstrm:
    # python3 or python2
    with open(join(dir_cur, 'README.md'), 'rb') as ifstrm:
        return ifstrm.read().decode("UTF-8")


setup(
    name=NAME,
    ## version=versioneer.get_version(),
    version='0.0.43',
    author='DV Klopfenstein, PhD',
    author_email='dvklopfenstein@protonmail.com',
    ## cmdclass=versioneer.get_cmdclass(),
    packages=PACKAGES,
    package_dir=PACKAGE_DIRS,
    # https://stackoverflow.com/questions/18787036/difference-between-entry-points-console-scripts-and-scripts-in-setup-py
    # https://stackoverflow.com/questions/45114076/python-setuptools-using-scripts-keyword-in-setup-py
    # https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#scripts
    scripts=glob('src/bin/*.py'),
    entry_points={
        'console_scripts':[
            'icite=pmidcite.scripts.icite:main',
            'summarize_papers=pmidcite.scripts.icite:summarize_papers',
        ],
    },
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
    description="Turbocharge a PubMed literature search using citation data from the NIH",
    # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=['requests'],
)

# Copyright (C) 2019, DV Klopfenstein, PhD. All rights reserved
