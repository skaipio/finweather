import os
from bisect import bisect_left
import fmi_forecast_api
from itertools import groupby
from operator import attrgetter, itemgetter
from common import Point

_latIndex, _lonIndex = 0, 1

class Forecaster:

    def fetchData(self):
        forecasts = fmi_forecast_api.getForecasts()
        self.__forecasts = {}
        self.__locations = []
        for location, forecastGroup in groupby(forecasts, attrgetter('location')):
            self.__locations.append(location)
            self.__forecasts[location] = list(forecastGroup)

        self.__sortedByLatitude = sorted(self.__locations)
        self.__sortedByLongitude = sorted(self.__locations, key=lambda location: tuple(reversed(location)))

    def findClosestForecastToPoint(self, point):
        iLat, closestByLatitude = Forecaster.__findClosestLocationToPointInPresortedList(self.__sortedByLatitude, point)
        iLon, closestByLongitude = Forecaster.__findClosestLocationToPointInPresortedList(self.__sortedByLongitude, point)

        smallestDistance, closestPoint = Forecaster.__findClosestPointToPoint(point, closestByLatitude, closestByLongitude)

        offsets = [iLat-1, iLat+1, iLon-1, iLon+1]
        while offsets != [-1,-1,-1,-1]:
            for i in range(0,4):
                locationIndex = offsets[i]
                data, key = (self.__sortedByLatitude, _latIndex) if i < 2 else (self.__sortedByLongitude, _lonIndex)
                if locationIndex >= 0 and locationIndex < len(data):
                    otherPoint = data[locationIndex]
                    if (otherPoint[key] - closestPoint[key])**2 <= smallestDistance:
                        offsets[i] += -1 if i % 2 else 1
                        smallestDistance, closestPoint = Forecaster.__getSmallerDistanceAndCloserPoint(smallestDistance, closestPoint, point, otherPoint)
                    else:
                        offsets[i] = -1

        return self.__forecasts[closestPoint]

    @staticmethod
    def __findClosestPointToPoint(exactPoint, *points):
        # Throw argument errors if points is empty
        pointsWithDistances = [(Forecaster.__getDistanceBetween(exactPoint, point), point) for point in points]
        sortedByDistance = sorted(pointsWithDistances, key=itemgetter(0))
        return sortedByDistance[0] if len(sortedByDistance) > 0  else (None, None)

    @staticmethod
    def __getSmallerDistanceAndCloserPoint(smallestDistance, closestPoint, queriedPoint, pointToCompareAgainst):
        d = Forecaster.__getDistanceBetween(queriedPoint, pointToCompareAgainst)
        if d < smallestDistance:
            return d, pointToCompareAgainst

        return smallestDistance, closestPoint

    @staticmethod
    def __findClosestLocationToPointInPresortedList(locations, point):
        i = bisect_left(locations, point)
        if i is not len(locations):
            return (i, locations[i])
        else:
            return None

    @staticmethod
    def __getDistanceBetween(point1, point2):
        return (point1[_latIndex]-point2[_latIndex])**2+(point1[_lonIndex]-point2[_lonIndex])**2
