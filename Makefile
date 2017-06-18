# Copyright (c) 2017 Massimo Mund <massimo.mund@lancode.de>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

python ?= python3.4
user ?= $(shell whoami)

all: spark.egg-info

spark.egg-info: setup.py bin/pip
	bin/pip install --editable . && touch $@
	bin/pip install -r requirements-venv.txt
bin/pip: bin/python
	curl https://bootstrap.pypa.io/get-pip.py | bin/python
bin/python:
	$(python) -m venv --without-pip .

test: all bin/coverage bin/flake8 bin/check-manifest
	bin/coverage run setup.py test
	bin/coverage html
	bin/coverage report --fail-under=100
	bin/flake8 setup.py spark
	bin/check-manifest || ! test -d .git
	bin/python setup.py check
bin/coverage: bin/pip
	bin/pip install coverage
bin/flake8: bin/pip
	bin/pip install flake8
bin/check-manifest: bin/pip
	bin/pip install check-manifest

docs: all bin/pdoc bin/pygmentize spark/** setup.py
	bin/pdoc --html --only-pypath --html-dir ./docs --overwrite spark spark
bin/pdoc: bin/pip
	bin/pip install pdoc
bin/pygmentize: bin/pip
	bin/pip install pygments

tox: bin/tox
	bin/tox -c tox.ini
bin/tox: bin/pip
	bin/pip install tox

man: man/spark.1

man/spark.1: spark.egg-info
	export USE_PKG_VERSION=1; \
	help2man -n "$(shell bin/python3 setup.py --description)" bin/spark > man/spark.1

ifdef DEB_HOST_ARCH
DESTDIR ?= /
PREFIX ?= usr/
install:
	$(python) setup.py install --no-compile --prefix="$(PREFIX)" --root="$(DESTDIR)" --install-layout=deb
else
DESTDIR ?= /
PREFIX ?= /usr/local
install:
	$(python) setup.py install --no-compile --prefix="$(PREFIX)"
endif

deb: man
	pdebuild --buildresult dist
	lintian --pedantic dist/*.deb dist/*.dsc dist/*.changes
	sudo chown -R $(user) dist/

clean:
	rm -rf $(shell find spark -name "__pycache__")
	rm -rf *.egg-info *.egg .eggs bin lib lib64 include share pyvenv.cfg pip-selfcheck.json
	rm -rf htmlcov .coverage
	rm -rf docs
	rm -rf .tox
	rm -rf build dist