#/***************************************************************************
# Easy Search
#
# Easy search features base on predefined layer and attribute
#
#                             -------------------
#        begin                : 2014-03-03
#        copyright            : (C) 2014 by Camptocamp SA
#        email                : info@camptocamp.com
# ***************************************************************************/
#
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/


###################CONFIGURE HERE########################
PLUGINNAME = easysearch
PACKAGES_NO_UI = widgets
PACKAGES = $(PACKAGES_NO_UI) ui
TRANSLATIONS = easysearch_de.ts easysearch_fr.ts

#this can be overiden by calling QGIS_PREFIX_PATH=/my/path make
DEFAULT_QGIS_PREFIX_PATH=/usr/local/qgis-master
###################END CONFIGURE#########################

PACKAGESSOURCES := $(shell find $(PACKAGES) -name "*.py")
SOURCES := easysearch_plugin.py $(PACKAGESSOURCES)
SOURCES_FOR_I18N = $(SOURCES:%=../%)

# QGIS PATHS
ifndef QGIS_PREFIX_PATH
export QGIS_PREFIX_PATH=$(DEFAULT_QGIS_PREFIX_PATH)
endif

export LD_LIBRARY_PATH:="$(QGIS_PREFIX_PATH)/lib:$(LD_LIBRARY_PATH)"
export PYTHONPATH:=$(PYTHONPATH):$(QGIS_PREFIX_PATH)/share/qgis/python:$(HOME)/.qgis2/python/plugins:$(CURDIR)/..:$(CURDIR)/lib/python2.7/site-packages/

ifndef QGIS_DEBUG
# Default to Quiet version
export QGIS_DEBUG=0
export QGIS_LOG_FILE=/dev/null
export QGIS_DEBUG_FILE=/dev/null
endif



default: compile
.PHONY: clean transclean help doc

help:
	@echo
	@echo "------------------"
	@echo "Available commands"
	@echo "------------------"
	@echo
	@echo make compile
	@echo make clean
	@echo make compile
	@echo make tests
	@echo make updatei18nconf
	@echo make transup
	@echo make transcompile
	@echo make package VERSION=\<version\> HASH=\<hash\>
	@echo make upload VERSION=\<version\>
	@echo make stylecheck
	@echo make pep8
	@echo make pylint

compile:
	@echo
	@echo "------------------------------"
	@echo "Compile ui and resources forms"
	@echo "------------------------------"
	make -C ui
	make -C resources

clean:
	@echo
	@echo "------------------------------"
	@echo "Clean ui and resources forms"
	@echo "------------------------------"
	rm -f *.pyc
	make clean -C ui
	make clean -C resources

################TESTS#######################
tests: stylecheck
	@echo
	@echo "------------------------------"
	@echo "Running test suite"
	@echo "------------------------------"
	export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH); \
	export PYTHONPATH=$(PYTHONPATH); \
	nosetests easysearch -v --with-id --with-coverage --cover-package=easysearch 3>&1 1>&2 2>&3 3>&- | grep -v "^Object::" || true


################TRANSLATION#######################
updatei18nconf:
	echo "SOURCES = " $(SOURCES_FOR_I18N) > i18n/i18n.generatedconf
	echo "TRANSLATIONS = " $(TRANSLATIONS) >> i18n/i18n.generatedconf
	echo "CODECFORTR = UTF-8"  >> i18n/i18n.generatedconf
	echo "CODECFORSRC = UTF-8"  >> i18n/i18n.generatedconf

# transup: update .ts translation files
transup:updatei18nconf
	pylupdate4 -noobsolete i18n/i18n.generatedconf
	rm -f i18n/i18n.generatedconf

# transcompile: compile translation files into .qm binary format
transcompile: $(TRANSLATIONS:%.ts=i18n/%.qm)

# transclean: deletes all .qm files
transclean:
	rm -f i18n/*.qm

%.qm : %.ts
	lrelease $<


################PACKAGE############################
# Create a zip package of the plugin named $(PLUGINNAME).zip.
# This requires use of git (your plugin development directory must be a
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=0.3.2 HASH=release-0.3.2
#   make package VERSION=0.3.2 HASH=master
#   make package VERSION=0.3.2 HASH=83c34c7d

package: transcompile compile
	rm -f $(PLUGINNAME).zip
	rm -rf $(PLUGINNAME)/
	mkdir -p $(PLUGINNAME)/ui/
	mkdir -p $(PLUGINNAME)/i18n/
	cp ui/*.py $(PLUGINNAME)/ui/
	cp i18n/*.qm $(PLUGINNAME)/i18n/
	git archive -o $(PLUGINNAME).zip --prefix=$(PLUGINNAME)/ $(HASH)
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/Makefile
	zip -d $(PLUGINNAME).zip $(PLUGINNAME)/.gitignore
	zip -g $(PLUGINNAME).zip $(PLUGINNAME)/*/*
	rm -rf $(PLUGINNAME)/
	mv $(PLUGINNAME).zip $(PLUGINNAME).$(VERSION).zip
	echo "Created package: $(PLUGINNAME).$(VERSION).zip"

################UPLOAD############################
# upload to qgis repo
PLUGIN_UPLOAD = $(CURDIR)/plugin_upload.py
upload: package
	$(PLUGIN_UPLOAD) $(PLUGINNAME).$(VERSION).zip


################VALIDATION#######################
# validate syntax style
stylecheck: pep8 pylint

pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E501 --exclude ui,lib,doc,sqlalchemy_schemadisplay.py resources . || true

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH); \
	export PYTHONPATH=$(PYTHONPATH); \
	pylint --output-format=parseable --reports=y --include-ids=y --rcfile=pylintrc $(PACKAGES_NO_UI) || true
