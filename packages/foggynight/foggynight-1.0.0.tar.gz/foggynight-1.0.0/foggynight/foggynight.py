import requests


class Weather:
    """Creates a Weather object getting an apikey as input
    and either a city name and country name or lat and lon coordinates.

    Package use example:

    # Create a weather object using a city name and a country name:
    # The api key below is not guaranteed too work.
    # Get your own apikey from https://openweathermap.org
    # And wait a couple of hours for the apikey to be activated

    # Using a city and a country name
    >>> weather1 = Weather(apikey="db4a34fbb9ac41777113a15776d2ea45", city = "Coram", country="USA")

    # Using latitude and longitude coordinates
    >>> weather2 = Weather(apikey="db4a34fbb9ac41777113a15776d2ea45", lat=41.1, lon=-4.1)

    # Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    # Simplified data for the next 12 hours:
    >>> weather1.next_12h_simplified()

    """
    def __init__(self, apikey, city=None, country=None, lat=None, lon=None):
        if city and country:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={apikey}&units=imperial"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=imperial"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("provide either a city and country or lat and lon arguments")
        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dictionary.
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, temperature, and sky condition every 3 hours
        for the next 12 hours as a tuple of tuples.
        """
        simple_data = []
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))
        return simple_data
