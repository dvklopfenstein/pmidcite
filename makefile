PYTHON = python3

findpy:
	find src -regextype posix-extended -regex ".*[a-z]+.py"
	find src -regextype posix-extended -regex "[a-z./]*" -type d

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

#### TESTS := \
####     src/tests/test_cfg_icite.py

pytest:
	make clobber_tmp
	python3.8 --version; python3.8 -m pytest --cov=pmidcite -v src/tests | tee pytest.log
	#### python3 -m pytest $(TESTS)

ver:
	git describe --tags --dirty --always

chk:
	chk_py
	chk_setup_dirs

cnt:
	find ./icite -name \*.py | wc -l
	find ./src/tests/icite -name \*.py | wc -l


# -----------------------------------------------------------------------------
# 1) Increase the version number:
vim_ver:
	vim -p src/pmidcite/__version__.py setup.py CHANGELOG.md

# 2) Create wheel - Check PyPi packages are up-to-date: make upgrade
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# universal wheels are pure Python
.PHONY: build
build:
	# python3 -m pip install --user --upgrade setuptools wheel
	make clean_dist
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel --universal
	ls -lh dist
	twine check dist/*

# 3) Upload wheel to PyPi
upload:
	twine upload dist/* --verbose


# -----------------------------------------------------------------------------
upgrade:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade setuptools wheel twine
	$(PYTHON) -m pip install --upgrade distutils

clean_dist:
	rm -rf dist build 

clean:
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
	rm -f src/tests/icite/*.py
	rm -f notebooks/pubmed_*.txt
	rm -f notebooks/p*.py
	rm -rf icite
	rm -rf notebooks/icite
	rm -rf src/tests/icite
	make clobber_tmp

clobber_tmp:
	rm -rf ./icite
	rm -rf ./src/tests/icite
