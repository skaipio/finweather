import requests
from datetime import datetime, timedelta
from xml.dom.minidom import parseString
from forecast import Forecast
from os import environ

apiKey = environ['FMI_API_KEY']

request = "getFeature"
storedQueryId = "fmi::forecast::hirlam::surface::cities::simple"
timeStep = 120
parameters = "temperature"

queryParams = {
    'request': request,
    'storedquery_id': storedQueryId,
    'timestep': timeStep,
    'parameters': parameters
}

forecastsBaseUrl = "http://data.fmi.fi/fmi-apikey/%s/wfs" % apiKey

previousFetchTime = datetime.min
positions = None
forecastXml = None

namespaceUris = {
    'wfs': 'http://www.opengis.net/wfs/2.0',
    'gml': 'http://www.opengis.net/gml/3.2',
    'BsWfs': 'http://xml.fmi.fi/schema/wfs/2.0'
}

def _findInElem(element, namespace, tag):
    return element.getElementsByTagNameNS(namespaceUris[namespace], tag)

def _parseForecast(wfsElement):
    position = _findInElem(wfsElement, 'gml', 'pos').item(0).firstChild.nodeValue.split()
    time = _findInElem(wfsElement, 'BsWfs', 'Time').item(0).firstChild.nodeValue
    value = _findInElem(wfsElement, 'BsWfs', 'ParameterValue').item(0).firstChild.nodeValue
    return Forecast(position, time, value)

def _parseTemperatureDataFromDom(dom):
    measurementElements = dom.getElementsByTagNameNS(namespaceUris['wfs'], 'member')
    return [_parseForecast(element) for element in measurementElements]

def getForecasts():
    global previousFetchTime, forecastXml
    if (datetime.now() - previousFetchTime).seconds > 5*60:
        print("Requesting fresh forecast data")
        forecastXml = requests.get(forecastsBaseUrl, params=queryParams)

    previousFetchTime = datetime.now()
    dom = parseString(forecastXml.content)

    return _parseTemperatureDataFromDom(dom)
