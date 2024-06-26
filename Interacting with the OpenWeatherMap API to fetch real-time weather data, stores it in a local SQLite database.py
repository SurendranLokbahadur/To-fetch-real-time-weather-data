import requests
import sqlite3
import datetime
from sqlite3 import Error

# OpenWeatherMap API endpoint and API key
API_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "YOUR_API_KEY"

def create_connection():
    """Creates a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect("weather_data.db")
        print("Connected to SQLite database.")
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    """Creates the weather_data table if it doesn't exist."""
    query = """CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                date TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                description TEXT NOT NULL
            );"""

    try:
        conn.execute(query)
        print("weather_data table created successfully.")
    except Error as e:
        print(e)

def fetch_weather_data(location):
    """Fetches real-time weather data for a given location."""
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"  # Use metric units for temperature
    }

    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        return temperature, humidity, description
    else:
        print("Failed to fetch weather data.")
        return None, None, None

def store_weather_data(conn, location):
    """Stores the fetched weather data in the SQLite database."""
