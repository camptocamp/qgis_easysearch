# -*- coding: utf-8 -*-
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


def classFactory(iface):
    # load easysearch class from file easysearch
    from easysearch_plugin import EasySearch
    return EasySearch(iface)
