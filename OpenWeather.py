import os
import requests

import sys
sys.path.append('/media/Data/dev/python-local-site')
from LocalAPIKeys import LAKReader

class OpenWeather:
    """
    This class is a wrapper around the OpeanWeather web api.
    See https://openweathermap.org/api

    To use this class:
    1. Instantiate an object of this class
    2. Call the get_weather method passing in a city name
       - city name can be a zip code or city, Country code (e.g. London, UK)
    3. Call any one or more of the following methods:
       - get_formatted_response method to get a 3 line weather description
       - get_weather_icon_file method to get the filename of the icon
         describing weather conditions.
       - get_weather_json to get the raw json response from openweather
    """
    def __init__(self):
        """
        Constructor that initializes object constants and defines objects
        used internally by objects of this class.
        """
        self.forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
        self.weather_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.weather_json = {}
        self.weather_api_key = ""

    def initialize(self):
        """
        Called to set the openweather API key.  The key is read from a file
        using the LocalAPIKeys.LAKReader class.
        Users of this object do not have to call this method directly.
        """
        rd = LAKReader()
        rd.read()
        self.weather_api_key = rd.getAPIKey('openweather')
        rd.clear()

        if len(self.weather_api_key) == 0:
            print("Cannot find openweather API Key.  Aborting...")
            sys.exit()


    def get_formatted_response(self):
        """
        Returns a 3 line string with the weather description for the city passed
        to the 'get_weather' method.
        The response will look similar to:
        City: Houston
        Conditions: scattered clouds
        Temperature (F): 94.93
        """
        if len(self.weather_json) == 0:
            return ""

        try:
            name = self.weather_json['name']
            desc = self.weather_json['weather'][0]['description']
            temp = self.weather_json['main']['temp']

            final_str = 'City: %s \nConditions: %s \nTemperature (F): %s' \
                        % (name, desc, temp)
        except:
            final_str = 'Could not find weather info.'

        return final_str


    def get_weather(self, city):
        """
        Performs an http request to openweather to get the current weather
        conditions for the passed in city.  The response from openweather
        is a json string which is stored internally.
        """
        self.weather_json = ""

        if len(self.weather_api_key) == 0:
            self.initialize()

        params = {'APPID': self.weather_api_key, 'q': city, 'units': 'imperial'}
        response = requests.get(self.weather_url, params=params)
        #    print(response.json())
        self.weather_json = response.json()


    def get_weather_icon_file(self):
        """
        Returns the file name of the icon associated to the last weather
        description returned from the call to get_weather. The file name
        returned will be a local file.
        """
        if len(self.weather_json) == 0:
            return ""

        icon_name = self.weather_json['weather'][0]['icon']
        loc = os.path.dirname(os.path.abspath(__file__))
        weather_icon_file = loc + os.path.sep + 'img' + os.path.sep + icon_name +'.png'

        return weather_icon_file

    def get_weather_json(self):
        """
        Returns the raw json openweather API response returned from the
        last call to get_weather.
        """
        return self.weather_json
