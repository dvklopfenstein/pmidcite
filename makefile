PYTHON = python3

install:
	pip3 install .

py:
	find src -name \*.py
	
e:
	find src/pmidcite/eutils -name \*.py

t:
	find src/tests -regextype posix-extended -regex ".*[a-z]+.py"

p:
	find src/bin src/pmidcite -name \*.py

d:
	find src -regextype posix-extended -regex "[a-z./]*" -type d

g:
	git status -uno
	git remote -v
	git branch

cli:
	find src/pmidcite/cli -name \*.py

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
	coverage run -m pytest -v src/tests --log-file=pytest.log
	#python3 --version; python3 -m pytest --cov=pmidcite -v src/tests | tee pytest.log
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

vim_md:
	vim -p README.md docs/index.md

# 2) Create wheel - Check PyPi packages are up-to-date: make upgrade
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# universal wheels are pure Python
#   Needs wheel package to run bdist_wheel: pip3 install wheel
.PHONY: build
build:
	# python3 -m pip install -U pip
	# python3 -m pip install --user --upgrade setuptools wheel
	make clean_build
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel --universal
	ls -lh dist
	twine check dist/*

# 3) Upload wheel to https://pypi.org
# https://pypi.org/manage/account/token/
# python3 -m pip install --upgrade pmidcite
upload:
	twine upload dist/* --verbose


# -----------------------------------------------------------------------------
upgrade:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade setuptools wheel twine
	$(PYTHON) -m pip install --upgrade distutils

clean_build:
	rm -rf dist build 

pyc:
	find . -name __pycache__ -type d | xargs rm -rf

clean:
	make pyc
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
	make clean_build

clobber_tmp:
	rm -rf ./icite
	rm -rf ./src/tests/icite

clobber:
	make -f makefile clobber_tmp clean_build
