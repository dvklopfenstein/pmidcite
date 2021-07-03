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
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

TESTS := \
    src/tests/test_cfg_icite.py

pytest:
	python3 -m pytest $(TESTS)

ver:
	git describe --tags --dirty --always

chk:
	chk_py
	chk_setup_dirs


# -----------------------------------------------------------------------------
# 1) Increase the version number:
vim_ver:
	vim -p src/pmidcite/__version__.py setup.py

# 2) Create wheel - Check PyPi packages are up-to-date: make upgrade
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# universal wheels are pure Python
sdist:
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
	rm -f test_eutils.cfg
	rm -f test_icite.cfg
	rm -f src/tests/icite/*.py
	rm -f notebooks/pubmed_*.txt
	rm -f notebooks/icite
	rm -f src/tests/icite
