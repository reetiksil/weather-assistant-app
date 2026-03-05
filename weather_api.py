import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    if not API_KEY:
        return {
            "success": False,
            "temp_c": None,
            "temp_f": None,
            "humidity": None,
            "cloud": None,
            "description": None,
            "message": "API key not configured."
        }

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    result = {
        "success": False,
        "temp_c": None,
        "temp_f": None,
        "humidity": None,
        "cloud": None,
        "description": None,
        "message": None
    }

    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        result["message"] = "Network error! \nPlease check your internet connection."
        return result

    if r.status_code != 200:
        result["message"] = f"Server Error: Status code {r.status_code}"
        return result

    datadic = r.json()

    if "error" in datadic:
        result["message"] = datadic["error"]["message"]
        return result

    result["success"] = True
    result["temp_c"] = datadic["current"]["temp_c"]
    result["temp_f"] = datadic["current"]["temp_f"]
    result["humidity"] = datadic["current"]["humidity"]
    result["cloud"] = datadic["current"]["cloud"]
    result["description"] = datadic["current"]["condition"]["text"]

    return result

