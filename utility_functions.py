
from qgis.core import *
import os.path
from PyQt4 import QtGui, uic

def getLegendLayers(iface, geom='all', provider='all'):
    """
    Return list of layer objects in the legend, with specific geometry type and/or data provider
    :param iface: QgsInterface
    :param geom: string ('point', 'linestring', 'polygon')
    :param provider: string
    :return: list QgsVectorLayer
    """
    layers_list = []
    for layer in iface.legendInterface().layers():
        add_layer = False
        if layer.isValid() and layer.type() == QgsMapLayer.VectorLayer:
            if layer.hasGeometryType() and (geom is 'all' or layer.geometryType() in geom):
                if provider is 'all' or layer.dataProvider().name() in provider:
                    add_layer = True
        if add_layer:
            layers_list.append(layer)
    return layers_list

def getLayersListNames(layerslist):
    layer_names = [layer.name() for layer in layerslist]
    return layer_names

def getLegendLayerByName(iface, name):
    layer = None
    for i in iface.legendInterface().layers():
        if i.name() == name:
            layer = i
    return layer

def getfieldByName(iface, name, layer):
    field = None
    for i in layer.dataProvider().fields():
        if i.name() == name:
            field = i
    return field

def getLegendLayerByIndex(iface, index):
    layer = None
    for i in iface.legendInterface().layers():
        if i.index() == index:
            layer = i
    return layer

def getFieldNames(layer):
    field_names = []
    if layer and layer.dataProvider():
        field_names = [field.name() for field in layer.dataProvider().fields()]
    return field_names

def getLayerPath(layer):
    path = ''
    provider = layer.dataProvider()
    provider_type = provider.name()
    if provider_type == 'spatialite':
        uri = QgsDataSourceURI(provider.dataSourceUri())
        path = uri.database()
    elif provider_type == 'ogr':
        uri = provider.dataSourceUri()
        path = os.path.dirname(uri)
    return path

def reloadLayer(layer):
    layer_name = layer.name()
    layer_provider = layer.dataProvider().name()
    new_layer = None
    if layer_provider in ('spatialite','postgres'):
        uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
        new_layer = QgsVectorLayer(uri.uri(), layer_name, layer_provider)
    elif layer_provider == 'ogr':
        uri = layer.dataProvider().dataSourceUri()
        new_layer = QgsVectorLayer(uri.split("|")[0], layer_name, layer_provider)
    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
    if new_layer:
        QgsMapLayerRegistry.instance().addMapLayer(new_layer)
    return new_layer

def isRequiredLayer(self, layer,type):
    if layer.type() == QgsMapLayer.VectorLayer \
            and layer.geometryType() == type:
            return True

    return False


def validatedDefaultSymbol(geometryType):
    symbol = QgsSymbolV2.defaultSymbol(geometryType)
    if symbol is None:
        symbol = QgsLineSymbolV2()

    return symbol

def makeSymbologyForRange(layer, min, max, label, colour, width):
    symbol = validatedDefaultSymbol(layer.geometryType())
    print symbol
    symbol.setColor(colour)
    symbol.setWidth(width)
    range = QgsRendererRangeV2(min, max, symbol, label)
    return range

def applySymbologyFixedDivisions(layer, field, min, max):
    rangeList = []

    rangeList.append(makeSymbologyForRange(layer, min, min+(.10 * (max-min)), str(min) + '-' + str(min+(.10 * (max-min))), QtGui.QColor("#ff0000"), 0.1))
    rangeList.append(makeSymbologyForRange(layer, min+(.10 * (max-min)), min+(.20 * (max-min)), str(min+(.10 * (max-min))) + '-' + str(min+(.20 * (max-min))), QtGui.QColor("#ff0000"), 0.3))
    rangeList.append(makeSymbologyForRange(layer, min+(.20 * (max-min)), min+(.30 * (max-min)), str(min+(.20 * (max-min))) + '-' + str(min+(.30 * (max-min))), QtGui.QColor("#ff0000"), 0.5))
    rangeList.append(makeSymbologyForRange(layer, min+(.30 * (max-min)), min+(.40 * (max-min)), str(min+(.30 * (max-min))) + '-' + str(min+(.40 * (max-min))), QtGui.QColor("#ff0000"), 0.7))
    rangeList.append(makeSymbologyForRange(layer, min+(.40 * (max-min)), min+(.50 * (max-min)), str(min+(.40 * (max-min))) + '-' + str(min+(.50 * (max-min))), QtGui.QColor("#ff0000"), 0.9))
    rangeList.append(makeSymbologyForRange(layer, min+(.50 * (max-min)), min+(.60 * (max-min)), str(min+(.50 * (max-min))) + '-' + str(min+(.60 * (max-min))), QtGui.QColor("#ff0000"), 1.1))
    rangeList.append(makeSymbologyForRange(layer, min+(.60 * (max-min)), min+(.70 * (max-min)), str(min+(.60 * (max-min))) + '-' + str(min+(.70 * (max-min))), QtGui.QColor("#ff0000"), 1.3))
    rangeList.append(makeSymbologyForRange(layer, min+(.70 * (max-min)), min+(.80 * (max-min)), str(min+(.70 * (max-min))) + '-' + str(min+(.80 * (max-min))), QtGui.QColor("#ff0000"), 1.5))
    rangeList.append(makeSymbologyForRange(layer, min+(.80 * (max-min)), min+(.90 * (max-min)), str(min+(.80 * (max-min))) + '-' + str(min+(.90 * (max-min))), QtGui.QColor("#ff0000"), 1.7))
    rangeList.append(makeSymbologyForRange(layer, min+(.90 * (max-min)),  max, str(min+(.90 * (max-min))) + '-' + str(max), QtGui.QColor("#ff0000"), 2.0))

    renderer = QgsGraduatedSymbolRendererV2(field, rangeList)
    #for i in renderer.symbols():
        #i.symbolLayer(0).setOutlineColor(QtGui.QColor("#ffffff"))
        #i.symbolLayer(0).setBorderWidth(0.000001)
        # i.symbolLayer(0).setOutputUnit(1)
    renderer.setMode(QgsGraduatedSymbolRendererV2.Custom)
    layer.setRendererV2(renderer)
    return renderer