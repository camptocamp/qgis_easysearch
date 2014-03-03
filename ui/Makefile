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

UI_FILES = $(wildcard *.ui)


###################### DON'T EDIT FURTHER ###################################

COMPILED_UI = $(UI_FILES:%.ui=%.py)

default : ui

clean:
	rm -f $(COMPILED_UI)
	rm -f *.pyc

ui: $(COMPILED_UI)

# Conversion rules

%.py : %.ui
	pyuic4 -o $@ $<
	sed -i "s/(_translate/(QtGui.QApplication.translate/" $@
