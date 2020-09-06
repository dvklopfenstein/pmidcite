

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

clean:
	rm -f test_eutils.cfg
	rm -f test_icite.cfg
	rm -f src/tests/icite/*.py
	rm -f notebooks/pubmed_*.txt
