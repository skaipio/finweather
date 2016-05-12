from flask import Flask, request, abort

import os
import locationDataImporter
import fmi_forecast
from forecastImporter import ForecastImporter

app = Flask(__name__)
locationData = locationDataImporter.getLocationData()
forecastData = ForecastImporter()
forecastData.fetchData()

@app.route("/forecast", methods=['GET'])
def forecast():
    locationRequested = request.args.get('location', '')
    if locationRequested is '':
        abort(404)

    location = locationData.searchLocation(locationRequested)

    if location is None or location is '':
        abort(404)
    else:
        closestForecasts = forecastData.findClosestForecastToPoint((location['latitude'], location['longitude']))
        return "<br>".join([str(forecast) for forecast in closestForecasts]) + "<br><br>" + str(location)

if __name__ == "__main__":
    app.run(debug=True)
