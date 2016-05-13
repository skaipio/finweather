import os, re
from operator import itemgetter
from bisect import bisect_left
from common import Point

_locationFilePath = os.path.join('FI', 'FI.txt')

_locationRegex = re.compile(r'^\d+" "|\t+([\w" "\-(),&\'/]+)\t+(?:[\w" "\-(),&\'/~:]+\t+)*(\d{1,2}(?:\.\d+)?)\t+(\d{1,2}(?:\.\d+)?)')

class Location:

    def __init__(self, name, point):
        self.name = name
        self.point = point

    def latitude(self):
        self.location.latitude

    def longitude(self):
        self.location.longitude

    def __str__(self):
        return "%s %s" % (self.name, str(self.point))

class LocationData:

    def __init__(self, rawData):
        self.__locationDictionary = {}

        for location in rawData:
            self.__locationDictionary[location.name] = location

        self.__locationNames = [location.name for location in rawData]
        self.__locationNames = sorted(self.__locationNames, key=lambda name: (str.lower(name), len(name)))

    def searchLocation(self, locationToSearch):
        locationName = self.__binarySearchLocation(locationToSearch)
        return self.__locationDictionary[locationName]

    def __binarySearchLocation(self, locationToSearch, lowerbound=None, upperbound=None, closestFound=None):
        searchAsLower = locationToSearch.lower()
        if upperbound == None:
            lowerbound = 0
            upperbound = len(self.__locationNames)-1
        midpoint = (lowerbound + upperbound) // 2
        midvalue = self.__locationNames[midpoint].lower()
        print(midvalue)
        if lowerbound == upperbound:
            return self.__locationNames[midpoint]
        elif searchAsLower < midvalue:
            return self.__binarySearchLocation(locationToSearch, lowerbound, midpoint-1, midpoint)
        elif searchAsLower > midvalue:
            return self.__binarySearchLocation(locationToSearch, midpoint+1, upperbound, midpoint)
        else:
            return self.__locationNames[midpoint]

def getLocationData():
    locationFile = open(_locationFilePath, 'r')
    lines = locationFile.readlines()
    locationFile.close()
    locations = []
    locationCount = 0

    for line in lines:
        mo = _locationRegex.search(line)
        if mo is not None:
            name, latitude, longitude = mo.groups()
            location = Location(name, (Point(float(latitude), float(longitude))))
            locations.append(location)
            locationCount += 1
        else:
            print("Could not match name, latitude and longitude in line:")
            print(line)

    print(str(locationCount) + " locations imported")
    return LocationData(locations)
