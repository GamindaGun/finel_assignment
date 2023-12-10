import sqlite3
import pprint
import requests
import os
from dotenv import load_dotenv

conn = sqlite3.connect('weather.db')
c = conn.cursor()

load_dotenv()
api_key = os.getenv('API_KEY_Openweather')
g_api_key = os.getenv('API_KEY_Google')

city_names = ["Corfe Castle UK", "OXford UK", "Lake District National Park UK", "The Cotswolds UK", "Cambridge UK",
              "Bristol UK", "Norwich UK", "Stonehenge UK", "Watergate Bay UK", "Birmingham UK"]

# Function to get weather data based on latitude and longitude using OpenWeatherMap API
def weather_lat_lon(city_name, g_api_key):
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={g_api_key}"
    google_response = requests.get(geo_url)

    if google_response.status_code == 200:
        google_data = google_response.json()
        location_data = google_data['results'][0]['geometry']['location']
        lat = (location_data['lat'])
        lon = (location_data['lng'])
        return lat, lon  # Return lat and lon


# Function to get latitude and longitude based on city name using Google Maps API
def get_lan_lon(lat, lon, API_key):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    return data


# Main function to be called when retrieving weather data
def main(city_name):
    city_weather_data = {}  #  # Initialize the dictionary here
    for city_name in city_names:
        lat, lon = weather_lat_lon(city_name, g_api_key)
        weather_data = get_lan_lon((lat), (lon), api_key)
        city_weather_data[city_name] = weather_data['list'] # Store data in the dictionary
    return city_weather_data # Return the populated dictionary


# Run the main function if executed as the main script
if __name__ == "__main__":
    city_weather_data = main(city_names)


    c.executescript('''
            DROP TABLE IF EXISTS WeatherData;
            CREATE TABLE WeatherData
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                clouds_all INT,
                Time INT,
                Day_Time CHAR,
                feels_like REAL,
                grnd_level REAL,
                humidity INT,
                pressure REAL,
                sea_level REAL,
                temp REAL,
                temp_kf REAL,
                temp_max REAL,
                temp_min REAL,
                pop REAL,
                rain_3h REAL,
                snow_3h REAL,
                sys_pod VARCHAR(10),
                visibility INT,
                weather_description VARCHAR(50),
                weather_icon VARCHAR(10),
                weather_id INT,
                weather_main VARCHAR(20),
                wind_deg INT,
                wind_gust REAL,
                wind_speed REAL,
                city_name VARCHAR(50))
    ''');

    # Insert data into the WeatherData table for each city
    for city, data_list in city_weather_data.items():
        for item in data_list:
            c.execute('''
                INSERT INTO WeatherData 
                (clouds_all, Time, Day_Time, feels_like, grnd_level, humidity, pressure, sea_level, temp, temp_kf, temp_max, temp_min, pop, rain_3h, snow_3h, sys_pod, visibility, weather_description, weather_icon, weather_id, weather_main, wind_deg, wind_gust, wind_speed, city_name) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
            ''', (
                item['clouds']['all'],
                item['dt'],
                item['dt_txt'],
                item['main']['feels_like'],
                item['main']['grnd_level'],
                item['main']['humidity'],
                item['main']['pressure'],
                item['main']['sea_level'],
                item['main']['temp'],
                item['main']['temp_kf'],
                item['main']['temp_max'],
                item['main']['temp_min'],
                item['pop'],
                item['rain']['3h'] if 'rain' in item and '3h' in item['rain'] else None,
                item['snow']['3h'] if 'snow' in item and '3h' in item['snow'] else None,
                item['sys']['pod'],
                item['visibility'],
                item['weather'][0]['description'],
                item['weather'][0]['icon'],
                item['weather'][0]['id'],
                item['weather'][0]['main'],
                item['wind']['deg'],
                item['wind']['gust'] if 'gust' in item['wind'] else None,
                item['wind']['speed'],
                city,

            ))

#Query The Database
c.execute("SELECT rowid, * FROM WeatherData")
fetch_items = c.fetchall()

for fetch_item in fetch_items:
    print(fetch_item)

# Commit the changes and close the connection
conn.commit()
conn.close()


