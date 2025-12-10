# Importing required modules
from flask import Flask, request, render_template
import redis
import requests
from dotenv import load_dotenv
import os
import json

# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

"""
Retrieve environment variables:
- API_KEY          : OpenWeather API key
- REDIS_NAME       : Hostname of Redis server (usually 'localhost')
- REDIS_PORT       : Port Redis is running on (default 6379)
- CACHE_TIME       : How long weather data should stay cached (in seconds)
- BASE_URL         : OpenWeather API base URL
"""

API_KEY    = os.getenv("API_KEY")
name       = os.getenv("REDIS_NAME")
port_num   = int(os.getenv("REDIS_PORT"))
cache_time = int(os.getenv("CACHE_TIME"))
url        = os.getenv("BASE_URL")

"""
Create Redis client object that connects to Redis server.

Parameters:
- host  : Redis server hostname (e.g., localhost)
- port  : Redis server port
- db    : Database index (0 is default)
- decode_responses=True ensures Redis returns strings instead of bytes
"""
client = redis.Redis(host=name, port=port_num, db=0, decode_responses=True)


"""
fetch_weather(city, country)

This function:
1. Checks Redis cache first to avoid unnecessary API calls.
2. If data exists in cache → returns cached result.
3. If not:
   - Calls OpenWeather API to fetch weather data.
   - Extracts only the required fields.
   - Stores this processed data in Redis with an expiry time.
4. Returns the weather data (either cached or fresh).

Parameters:
- city     : city name in lowercase
- country  : country name in lowercase
"""
def fetch_weather(city, country):

    # Create a unique cache key for the city-country combination
    cache_key = f"weather:{city},{country}"

    # Attempt to fetch cached data
    cached_data = client.get(cache_key)
    if cached_data:
        print("[From cache]\n")
        data = json.loads(cached_data)  # Convert JSON string back to dict
        print(data)
        return data

    # API parameters for requesting weather data
    params = {
        'q': f"{city},{country}",
        'appid': API_KEY,
        'units': "metric"
    }

    # Make API call to OpenWeather
    response = requests.get(url, params=params)

    # If API returns error
    if response.status_code != 200:
        print("API Error:", response.status_code)
        return None

    # Extract only required fields from full JSON response
    body = response.json()
    data = {
        'name':       body.get('name'),
        'temperature': body['main']['temp'],
        'feels_like':  body['main']['feels_like'],
        'humidity':    body['main']['humidity'],
        'pressure':    body['main']['pressure'],
        'wind':        body['wind']['speed'],
        'clouds':      body['clouds']['all'],
        'timezone':    body['timezone'],
    }

    print("[From API]\n")
    print(data)

    # Store processed data in Redis with expiration time
    client.setex(cache_key, cache_time, json.dumps(data))

    return data


"""
Route: "/"
This route handles the homepage.
It displays the input form where the user enters the location.
"""
@app.route("/")
def index():
    return render_template("index.html")


"""
Route: "/weather"
This route receives the city input from the user.

Steps:
1. Read "city" query parameter from form.
2. Validate the input format.
3. Split into city + country.
4. Fetch weather using fetch_weather().
5. Render weather_info.html with the returned data.
"""
@app.route("/weather")
def weather():

    # Get user input from query parameter
    info = request.args.get("city")

    if not info:
        return "Invalid input. Try e.g. Hyderabad,IN"

    # Safe split into city + country
    try:
        city, country = [x.strip().lower() for x in info.split(",", 1)]
    except ValueError:
        return "Invalid format. Use City,Country (e.g. Hyderabad,IN)"

    # Fetch weather data (either cached or fresh)
    data = fetch_weather(city, country)

    # Handle incorrect city or API error
    if data is None:
        return "Could not fetch weather. Please check city name."

    return render_template("weather_info.html", data=data)


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
