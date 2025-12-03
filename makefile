PYTHON = python3

install:
	pip3 install .

py:
	find src/bin -name \*.py
	find pmidcite -name \*.py
	find tests -name \*.py | grep -v icite
	
e:
	find pmidcite/eutils -name \*.py

t:
	find tests -regextype posix-extended -regex ".*[a-z]+.py"

p:
	find src/bin pmidcite -name \*.py

d:
	find src -regextype posix-extended -regex "[a-z./]*" -type d

cli:
	find pmidcite/cli -name \*.py

diff0:
	git diff --compact-summary

cfg:
	python3 -c 'from pmidcite.cfgparser.eutils import EUtilsCfgFile; EUtilsCfgFile().wr_rc()'
	python3 -c 'from pmidcite.cfgparser.icite import NIHiCiteCfgFile; NIHiCiteCfgFile().wr_rc()'

# -----------------------------------------------------------------------------
pylint:
	@git status -uno | perl -ne 'if (/(\S+\.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

pytest:
	make clobber_tmp
	python3 --version
	coverage run -m pytest -v -r y --log-file=pytest.log --full-trace tests

ver:
	git describe --tags --dirty --always

chk:
	chk_py
	chk_setup_dirs

cnt:
	find icite -name \*.py | wc -l
	find tests/icite -name \*.py | wc -l


# -----------------------------------------------------------------------------
# 1) Increase the version number:
vim_ver:
	vim -p pyproject.toml pmidcite/__init__.py CHANGELOG.md

vim_md:
	vim -p README.md docs/index.md


# -----------------------------------------------------------------------------
clean_build:
	rm -rf dist build 

pyc:
	find . -name __pycache__ -type d | xargs rm -rf
	find . -name .ipynb_checkpoints | xargs rm -rf
	rm -rf notebooks/icite; mkdir notebooks/icite

clean:
	make pyc
	rm -f *.log
	rm -f notebooks/pubmed_20050301.txt
	rm -f pubmed_20050301.txt
	rm -f 29129787.txt
	rm -f 29628312.txt
	rm -f dnldr_*.txt
	rm -f SMILES_review.txt
	rm -f final_cite.txt
	rm -f p*.py
	rm -f pubmed_*.txt
	rm -f test_eutils.cfg
	rm -f test_icite.cfg
	rm -f tests/icite/*.py
	rm -f notebooks/pubmed_*.txt
	rm -f notebooks/p*.py
	rm -rf icite
	rm -rf notebooks/icite
	rm -rf tests/icite
	make clobber_tmp
	make clean_build
	make pyc

clobber_tmp:
	rm -rf icite
	rm -rf tests/icite

clobber:
	make -f makefile clean clobber_tmp clean_build pyc
