from ..module import Module

try: import requests 
except: print("ModuleWeather: requests module not found!")

class ModuleWeather(Module):

    def __init__(self,  api_key: str, str_format: str="{city}: {temp}°({feels_like}°) {weather}",
                        city: str="London", country: str="UK",
                        periodic: float=600.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format = str_format
        self.city       = city
        self.country    = country
        self.api_key    = api_key

    def get_weather_icon(self, weather_js) -> str:
        """
        icons from: https://github.com/erikflowers/weather-icons
        """
        icon_url = weather_js['weather'][0]['icon']
        weather_icons = { 
            "01d" : "",
            "01n" : "",
            "02d" : "",
            "02n" : "",
            "03*" : "",
            "04*" : "",
            "09d" : "",
            "09n" : "",
            "10d" : "",
            "10n" : "",
            "11d" : "",
            "11n" : "",
            "13d" : "",
            "13n" : "",
            "50d" : "",
            "50n" : "",
        }
        if icon_url in weather_icons.keys():
            return weather_icons[icon_url]
        return ""

    def execute(self) -> str:
        loc_url     = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.country}&limit=1&appid={self.api_key}"
        loc_js      = requests.get(loc_url).json()
        lat, lon    = loc_js[0]['lat'], loc_js[0]['lon']
        
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        weather_js  = requests.get(weather_url).json()

        result = self.str_format
        for key, value in weather_js['main'].items():
            data = str(round(value, 1))
            result = result.replace("{"+key+"}", data)
        result = result.replace("{city}", self.city)
        result = result.replace("{weather}", self.get_weather_icon(weather_js))
        return result



