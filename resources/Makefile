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


RESOURCE_FILES = resources.qrc

###################### DON'T EDIT FURTHER ###################################

COMPILED_RESOURCES = $(RESOURCE_FILES:%.qrc=%_rc.py)
MOVED_COMPILED_RESOURCES = $(RESOURCE_FILES:%.qrc=../ui/%_rc.py)

default : resources

clean:
	rm -f $(MOVED_COMPILED_RESOURCES)
	rm -f *.pyc

resources: $(COMPILED_RESOURCES)
	mv resources_rc.py ../ui

# Conversion rules

%_rc.py : %.qrc
	pyrcc4 -o $@ $<
