BUILDDIR?=~build
BUILD_NUMBER=0
DATABASE_URL?=

help:
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make clean                       remove the generated files         '
	@echo '   make fullclean                   clean + remove tox, cache          '
	@echo '   make coverage                    run coverage                       '
	@echo '   make test                        run tests                          '
	@echo '   make develop                     update develop environment         '
	@echo '                                                                       '


.mkbuilddir:
	mkdir -p ${BUILDDIR}


.init-db:
	# initializing '${DBENGINE}' database '${DBNAME}'
	psql -c 'DROP DATABASE IF EXISTS test_unicef_security;' -U postgres -h 127.0.0.1
	psql -c 'DROP DATABASE IF EXISTS unicef_security;' -U postgres -h 127.0.0.1
	psql -c 'CREATE DATABASE unicef_security;' -U postgres -h 127.0.0.1


develop:
	@${MAKE} clean
	pipenv install -e .[test] --skip-lock


clean:
	# cleaning
	@rm -rf ${BUILDDIR} .pytest_cache src/unicef_security.egg-info dist *.xml .cache *.egg-info .coverage .pytest MEDIA_ROOT MANIFEST .cache *.egg build STATIC
	@find . -name __pycache__  -prune | xargs rm -rf
	@find . -name "*.py?" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml


fullclean:
	rm -fr .tox
	rm -f *.sqlite
	make clean


lint:
	-flake8 src/ tests/
	-isort src/ tests/ --check-only -rc


test:
	pipenv run pytest tests/ src/ \
            --cov=unicef_security \
            --cov-config=tests/.coveragerc \
            --cov-report=html \
            --cov-report=term
