# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Desirelines
                                 A QGIS plugin
 Create the desire lines from a space Syntax accessibility analysis
                             -------------------
        begin                : 2018-02-28
        copyright            : (C) 2018 by AA/Space Syntax Limited
        email                : a.acharya@spacesyntax.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Desirelines class from file Desirelines.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Desire_lines import Desirelines
    return Desirelines(iface)
