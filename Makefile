DEPS = server-core
VIRTUALENV = virtualenv
PYTHON = bin/python
NOSE = bin/nosetests -s
TESTS = syncwhoami/tests
BUILDAPP = bin/buildapp
BUILDRPMS = bin/buildrpms
BUILD_TMP = /tmp/server-storage-build.${USER}
PYPI = http://pypi.python.org/simple
PYPIOPTIONS = -i $(PYPI)
CHANNEL = dev
INSTALL = bin/pip install
INSTALLOPTIONS = -U -i $(PYPI)

ifdef PYPIEXTRAS
	PYPIOPTIONS += -e $(PYPIEXTRAS)
	INSTALLOPTIONS += -f $(PYPIEXTRAS)
endif

ifdef PYPISTRICT
	PYPIOPTIONS += -s
	ifdef PYPIEXTRAS
		HOST = `python -c "import urlparse; print urlparse.urlparse('$(PYPI)')[1] + ',' + urlparse.urlparse('$(PYPIEXTRAS)')[1]"`

	else
		HOST = `python -c "import urlparse; print urlparse.urlparse('$(PYPI)')[1]"`
	endif
	INSTALLOPTIONS += --install-option="--allow-hosts=$(HOST)"

endif

INSTALL += $(INSTALLOPTIONS)


.PHONY: all build update test build_rpms


all:	build

build:
	$(VIRTUALENV) --distribute --no-site-packages .
	$(INSTALL) Distribute
	$(INSTALL) MoPyTools
	$(INSTALL) Nose
	$(INSTALL) WebTest
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)
	# py-scrypt doesn't play nicely with pypi2rpm
	# so we can't list it in the requirements files.
	mkdir -p ${BUILD_TMP}
	cd ${BUILD_TMP}; tar -xzvf $(CURDIR)/upstream-deps/py-scrypt-0.6.0.tar.gz
	$(INSTALL) ${BUILD_TMP}
	rm -rf ${BUILD_TMP}

update:
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)

test:
	$(NOSE) $(TESTS)

build_rpms:
	$(BUILDRPMS) -c $(CHANNEL) $(DEPS)
	# py-scrypt doesn't play nicely with pypi2rpm.
	cd ${BUILD_TMP}; tar -xzvf $(CURDIR)/upstream-deps/py-scrypt-0.6.0.tar.gz
	cd ${BUILD_TMP}; python setup.py  --command-packages=pypi2rpm.command bdist_rpm2 --binary-only --name=python26-scrypt --dist-dir=$(CURDIR)/rpms

