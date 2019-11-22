
findpy:
	find src -regextype posix-extended -regex ".*[a-z]+.py"
	find src -regextype posix-extended -regex "[a-z./]*" -type d

diff0:
	git diff --compact-summary

pylint:
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

