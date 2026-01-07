#
# HP35Stack Makefile (part of CNC project)
#

# Make us OS-independent ... at least for MacOS and Linux
OS := $(shell uname -s)
ifeq (Linux, ${OS})
    DATE := $(shell date --iso-8601)
else
    DATE := $(shell date "+%Y-%m-%d")
endif

# Python version
PYTHON := python3
# PYTHON := python2
# PYLINT := ${PYTHON} -m pylint
PYLINT := pylint

HERE := $(shell pwd)

.PHONY: help
help:
	cat Makefile
	@ echo "OS: " ${OS}
	@ echo "PYTHON: " ${PYTHON}
	@ echo "DATE: " ${DATE}
	@ echo "HERE: " ${HERE}

PYTHON_SOURCE = \
	hp35stack.py \
	pyproject.toml

FILES = \
	${PYTHON_SOURCE} \
	LICENSE \
	Makefile \
	pylintrc \
	README.md

.PHONY: clean pylint listings test lint

clean:
	- rm *.ps *.pdf

pylint:
	- ${PYLINT} hp35stack.py

lint: pylint

.PHONY: test
test:
	${PYTHON} hp35stack.py

listings: listing-hp35stack.pdf listing-Makefile.pdf
	mv $^ ~/tmp

listing-%.ps: %.py
	enscript -G $< -p $@

listing-Makefile.ps: Makefile
	enscript -G $< -p $@

%.pdf: %.ps
	ps2pdf $< $@
	rm $<

# GIT operations

diff: .gitattributes
	git diff

status: ${FORCE}
	git status

# this brings the remote copy into sync with the local one
commit: .gitattributes
	git commit ${FILES}
	git push -u origin main

# This brings the local copy into sync with the remote (main)
pull: .gitattributes
	git pull origin main

log: .gitattributes
	git log --pretty=oneline
