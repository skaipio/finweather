from flask import Flask, request, abort

import os
import location_data_import
import fmi_forecast

app = Flask(__name__)
locationData = location_data_import.getLocationData()
locationDictionary = {}
for location in locationData:
    locationDictionary[location['name']] = location

locationNames = [location['name'] for location in locationData]
locationNames = sorted(locationNames, key=str.lower)

def binarySearchLocation(locationToSearch, lowerbound=None, upperbound=None):
    searchAsLower = locationToSearch.lower()
    if upperbound == None:
        lowerbound = 0
        upperbound = len(locationNames)-1
    midpoint = (lowerbound + upperbound) // 2
    midvalue = locationNames[midpoint].lower()
    print(midvalue)
    if midvalue.startswith(searchAsLower):
        return locationNames[midpoint]
    elif lowerbound == upperbound:
        return None
    elif searchAsLower < midvalue:
        return binarySearchLocation(locationToSearch, lowerbound, midpoint-1)
    elif searchAsLower > midvalue:
        return binarySearchLocation(locationToSearch, midpoint+1, upperbound)
    else:
        return None

@app.route("/forecast", methods=['GET'])
def hello():
    locationRequested = request.args.get('location', '')
    if locationRequested is '':
        abort(404)

    location = binarySearchLocation(locationRequested)
    if location is '':
        abort(404)
    else:
        return str(locationDictionary[location])

if __name__ == "__main__":
    app.run(debug=True)
