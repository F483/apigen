# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


help:
	@echo "Some usefull development shortcuts."
	@echo "  clean      Remove all generated files."
	@echo "  test       Run tests and analisys tools."
	@echo "  devsetup   Setup development environment."
	@echo "  build      Build package."
	@echo "  publish    Upload package to pypi."


clean:
	@rm -rf env
	@rm -rf apigen.egg-info
	@rm -rf build
	@rm -rf dist
	@find | grep -i ".*\.pyc$$" | xargs -r -L1 rm


devsetup: clean
	# TODO python 2 venv
	# TODO python 3 venv
	python setup.py develop


test: devsetup
	# TODO add static analisys 
	# TODO add lint 
	# TODO add tests


build: test
	python setup.py register sdist


publish: build
	python setup.py upload


