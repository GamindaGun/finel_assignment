# import necessary library.
import requests
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load OpenWeatherMap API key from environment variables
load_dotenv()
api_key = os.getenv('API_KEY_Openweather')


# Define a data class to structure weather information
@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float
    humidity: int
    temp_max: int
    temp_min: int
    wind_degree: int
    wind_gust: int
    wind_speed: int
    date_time: int


# Function to get latitude and longitude based on city name using Google Maps API
def get_lan_lon(lat, lon, API_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        final_data = WeatherData(
            main=data.get('weather')[0].get('main'),
            description=data.get('weather')[0].get('description'),
            icon=data.get('weather')[0].get('icon'),
            temperature=round(data.get('main').get('temp')),
            humidity=data.get('main').get('humidity'),
            temp_max=round(data.get('main').get('temp_max')),
            temp_min=round(data.get('main').get('temp_min')),
            wind_degree=data.get('wind').get('deg'),
            wind_gust=data.get('wind').get('gust'),
            wind_speed=data.get('wind').get('speed'),
            date_time=data.get('dt')
        )
        return final_data

def forecast_weather(lat, lon, API_key):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        forecast = response.json()
        list_data = forecast.get('list', [])

        forecast_data = []
        for item in list_data:
            weather_data = {
                'main': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'temperature': round(item['main']['temp']),
                'humidity': item['main']['humidity'],
                'temp_max': round(item['main']['temp_max']),
                'temp_min': round(item['main']['temp_min']),
                'wind_degree': item['wind']['deg'],
                'wind_gust': item['wind']['gust'],
                'wind_speed': item['wind']['speed'],
                'date_time': item['dt_txt']
            }
            forecast_data.append(weather_data)

        return forecast_data
    else:
        return None


# Obtain Google API Key from envfile.
load_dotenv()
g_api_key = os.getenv('API_KEY_Google')


# Function to get weather data based on latitude and longitude using OpenWeatherMap API
def weather_lat_lon(city_name, g_api_key):
    geo_url = (f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={g_api_key}")
    google_response = requests.get(geo_url)

    if google_response.status_code == 200:
        google_data = google_response.json()
        location_data = google_data['results'][0]['geometry']['location']
        lat = (location_data['lat'])
        lon = (location_data['lng'])
        return lat, lon


# Main function to be called when retrieving weather data
def main(city_name):
    lat, lon = weather_lat_lon(city_name, g_api_key)
    weather_data = get_lan_lon((lat), (lon), api_key)
    forecast = forecast_weather((lat), (lon), api_key)
    return weather_data, forecast


# Run the main function if executed as the main script
if __name__ == "__main__":
    lat, lon = weather_lat_lon('city_name', g_api_key)
    print(get_lan_lon(float(lat), float(lon), api_key))

