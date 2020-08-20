#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""For installing pmidcite package and accompanying scripts."""

from distutils.core import setup
import versioneer
from glob import glob


setup(
    name='pmidcite',
    version=versioneer.get_version(),
    author='DV Klopfenstein',
    author_email='dvklopfenstein@protonmail.com',
    long_description=(
        'Augment your literature search '
        'from the command-line to link '
        "citation data from NIH's iCite "
        'with PubMed IDs (PMIDs), '
        'rather than clicking and clicking and clicking on '
        """Google Scholar's "Cited by N" links.\n\n"""
        'https://github.com/dvklopfenstein/pmidcite/blob/master/README.md'),
    cmdclass=versioneer.get_cmdclass(),
    packages=['pmidcite',],
    package_dir={'pmidcite': 'src/pmidcite'},
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
