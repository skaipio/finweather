class Forecast:
    """ A class for forecast data. """
    def __init__(self, location, time, estimation):
        self.location = location
        self.time = time
        self.estimation = estimation

    def __str__(self):
        return "Forecast estimated %s\u00b0C at %s, %s" % (self.estimation, self.location, self.time)
