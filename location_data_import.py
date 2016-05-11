import os

locationFilePath = os.path.join('FI', 'FI.txt')
locationData = []

def getLocationData():
    if len(locationData) == 0:
        locationFile = open(locationFilePath, 'r')
        lines = locationFile.readlines()
        locationFile.close()

        for line in lines:
            fields = line.split('\t')
            locationData.append({
                'name': fields[1],
                'latitude': fields[4],
                'longitude': fields[5]
            })

    return locationData
