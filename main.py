from flask import Flask, request, abort

import os
import locations
import fmi_forecast_api
from forecasting import Forecaster

app = Flask(__name__)
locationData = locations.getLocationData()
forecaster = Forecaster()
forecaster.fetchData()

@app.route("/forecast", methods=['GET'])
def forecast():
    locationRequested = request.args.get('location', '')
    if locationRequested is '':
        abort(404)

    location = locationData.searchLocation(locationRequested)

    if location is None:
        abort(404)
    else:
        closestForecasts = forecaster.findClosestForecastToPoint(location.point)
        return "<br>".join([str(forecast) for forecast in closestForecasts]) + "<br><br>" + str(location)

if __name__ == "__main__":
    app.run(debug=True)
