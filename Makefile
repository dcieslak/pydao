NAME=pydao
VER=0.9.3

all: dynamic-check doc/pydao-userguide.html

F9: all
F10: static-check

static-check: pylint

dynamic-check:
	@echo dynamic-check
	@time -p python -tt test.py

clean:
	rm `find . -name \*.pyc -o -name \*.log -o -name \*.bak`


t:
	ctags pydao/*.py

coverage:
	@echo coverage
	@python lib/coverage.py -x test.py \
		`ls -t \`grep -lr "^def test" pydao/*.py\``
	@python lib/coverage.py -r -m pydao/*.py | tee doc/pydao-coverage.txt

doc/%.txt: pydao/%.py
	cat $< > $@

gendoc: doc/AbstractDaoTest.txt doc/SqlDaoTest.txt doc/pydao-userguide.html
	pydoc -w\
		pydao.AbstractDao \
		pydao.SqlDao \
		pydao.MysqlDao \
		pydao.PostgresqlDao \
		pydao.Condition \
		pydao.InRangeCondition \
		pydao.InSequenceCondition \
		pydao.IsNullCondition \
		pydao.NotNullCondition \
		pydao.ArbitraryCondition \
		pydao.LikeCondition \
		pydao.SimpleDao \
		pydao.InMemoryDao
	mv pydao*html doc

%.html: %.shtml utils/doc.awk pydao/GuideTest.py
	awk -f utils/doc.awk $< > $@

#######################################################################
# Databases
#######################################################################
db-mysql-init:
	mysql -u root < sql/test-init-mysql.sql
	mysql -u pydao -ppydao pydao < sql/test-scheme-mysql.sql

db-postgresql-init:
	psql -q template1 postgres < sql/test-scheme-postgresql.sql

db-init: db-mysql-init db-postgresql-init

pylint:
	@python run_pylint.py \
		--reports=n \
		--ignore=imports.py \
		--rcfile=.pylintrc \
		--include-ids=y \
		-f parseable \
		pydao/*.py

di2:
	cvs di -uN | show-color-diff

up:
	cvs up 2>&1 | show-color-diff

deploy: coverage gendoc
	echo HIT CTRL-C TO BREAK
	rm -f /tmp/$(NAME)-$(VER);
	ln -sf `pwd` /tmp/$(NAME)-$(VER);
	cd /tmp; tar zcvf $(NAME)-$(VER).tgz $(NAME)-$(VER)\
		--dereference\
		--exclude-from=$(NAME)-$(VER)/.deploy-exclude
	cd /tmp; rm -f  $(NAME)-$(VER).zip;\
	zip -r $(NAME)-$(VER).zip $(NAME)-$(VER)\
		-x@$(NAME)-$(VER)/.deploy-exclude
	pftp -i < upload.ftp

f:
	firefox doc/index.html


git:
	git-prune
	git-repack


