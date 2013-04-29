DEPS = server-core
VIRTUALENV = virtualenv
PYTHON = bin/python
NOSE = bin/nosetests -s
TESTS = syncwhoami/tests
BUILDAPP = bin/buildapp
BUILDRPMS = bin/buildrpms
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

update:
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)

test:
	$(NOSE) $(TESTS)

build_rpms:
	$(BUILDRPMS) -c $(CHANNEL) $(DEPS)
