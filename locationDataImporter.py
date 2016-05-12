import os, re
from operator import itemgetter
from bisect import bisect_left

locationFilePath = os.path.join('FI', 'FI.txt')

_keyLat = 'latitude'
_keyLon = 'longitude'

_locationRegex = re.compile(r'^\d+\s+(\w+)\s+\D+(\d{1,2}\.\d+)\s+(\d{1,2}\.\d+)')

class LocationData:

    def __init__(self, rawData):
        self.__sortedByLatitude = sorted(rawData, key=itemgetter(_keyLat, _keyLon))
        self.__sortedByLongitude = sorted(rawData, key=itemgetter(_keyLon, _keyLat))
        self.__sortedLatitude = [item[_keyLat]*180+item[_keyLon] for item in self.__sortedByLatitude]
        self.__sortedLongitude = [item[_keyLon]*180+item[_keyLat] for item in self.__sortedByLongitude]
        self.__locationDictionary = {}

        for location in rawData:
            self.__locationDictionary[location['name']] = location

        self.__locationNames = [location['name'] for location in rawData]
        self.__locationNames = sorted(self.__locationNames, key=lambda name: (str.lower(name), len(name)))

    def findClosestPoint(self, point):

        iLat, closestByLatitude = self.__findClosestByLatitude(point)
        iLon, closestByLongitude = self.__findClosestByLongitude(point)

        print("closest by latitude: " + str(closestByLatitude))
        print("closest by longitude: " + str(closestByLongitude))

        latDistance = self.__getDistanceBetween(point, closestByLatitude)
        lonDistance = self.__getDistanceBetween(point, closestByLongitude)
        closestPoint = closestByLatitude
        smallestDistance = latDistance
        if lonDistance < latDistance:
            closestPoint = closestByLongitude
            smallestDistance = lonDistance

        offsets = [iLat-1, iLat+1, iLon-1, iLon+1]
        while offsets != [-1,-1,-1,-1]:
            for i in range(0,4):
                data = self.__sortedByLatitude if i < 2 else self.__sortedByLongitude
                if offsets[i] >= 0 and offsets[i] < len(data):
                    value = data[offsets[i]]
                    key = _keyLat if i < 2 else _keyLon
                    if (value[key] - closestPoint[key])**2 <= smallestDistance:
                        d = self.__getDistanceBetween(point, value)
                        if d < smallestDistance:
                            smallestDistance = d
                            closestPoint = value
                            print("found point closer: " + str(closestPoint))
                        offsets[i] += -1 if i % 2 else 1
                    else:
                        offsets[i] = -1

        return closestPoint

    def searchLocation(self, locationToSearch):
        locationName = self.__binarySearchLocation(locationToSearch)
        return self.__locationDictionary[locationName]

    def __binarySearchLocation(self, locationToSearch, lowerbound=None, upperbound=None):
        searchAsLower = locationToSearch.lower()
        if upperbound == None:
            lowerbound = 0
            upperbound = len(self.__locationNames)-1
        midpoint = (lowerbound + upperbound) // 2
        midvalue = self.__locationNames[midpoint].lower()
        print(midvalue)
        if midvalue.startswith(searchAsLower):
            return self.__locationNames[midpoint]
        elif lowerbound == upperbound:
            return None
        elif searchAsLower < midvalue:
            return self.__binarySearchLocation(locationToSearch, lowerbound, midpoint-1)
        elif searchAsLower > midvalue:
            return self.__binarySearchLocation(locationToSearch, midpoint+1, upperbound)
        else:
            return None

    def __findClosestByLatitude(self, point):
        i = bisect_left(self.__sortedLatitude, point[_keyLat]*180+point[_keyLon])
        return (i, self.__sortedByLatitude[i])

    def __findClosestByLongitude(self, point):
        i = bisect_left(self.__sortedLongitude, point[_keyLon]*180+point[_keyLat])
        return (i, self.__sortedByLongitude[i])

    def __getDistanceBetween(self, point1, point2):
        return (point1[_keyLat]-point2[_keyLat])**2+(point1[_keyLon]-point2[_keyLon])**2

def getLocationData():
    locationFile = open(locationFilePath, 'r')
    lines = locationFile.readlines()
    locationFile.close()
    locationData = []

    for line in lines:
        mo = _locationRegex.search(line)
        if mo is not None:
            name, latitude, longitude = mo.groups()
            locationData.append({
                'name': name,
                'latitude': float(latitude),
                'longitude': float(longitude)
            })

    return LocationData(locationData)
