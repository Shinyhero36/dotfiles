import requests
from datetime import datetime
import json

LON = 1.44
LAT = 43.60
TODAY = datetime.now().strftime("%Y-%m-%d")
HH = datetime.now().strftime("%H")

URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,windspeed_10m&daily=weathercode,sunrise,sunset&start_date={TODAY}&end_date={TODAY}&timezone=auto"


def is_day(sunrise: str, sunset: str):
    """Check if it's day or night

    Args:
        sunrise (str): sunrise time
        sunset (str): sunset time
    """
    sunrise = datetime.strptime(sunrise, "%Y-%m-%dT%H:%M")
    sunset = datetime.strptime(sunset, "%Y-%m-%dT%H:%M")
    now = datetime.now()

    return sunrise < now < sunset


def is_windy(speed: float):
    """Check if it's windy

    Args:
        speed (int): wind speed in km/h
    """
    return speed > 33.0


def find_icon(weather_code: int, windspeed: float, day: bool):
    """Select the icon to display based on the weather code

    Args:
        weather_code (int): the weather code
        windspeed (float): the wind speed in km/h
        day (bool): if it's day or night

    Note:
        More info on weather codes: https://open-meteo.com/en/docs
        Icons are from: https://bas.dev/work/meteocons
    """
    if is_windy(windspeed):
        return "wind.svg"
    match weather_code:
        case 0:  # Clear sky
            return f"clear{'-day' if day else '-night'}.svg"
        case 1:  # mainly clear
            return f"clear{'-day' if day else '-night'}.svg"  # TODO: Find a better icon
        case 2:  # Partly cloudy
            return f"partly-cloudy-{'day' if day else 'night'}.svg"
        case 3:  # overcast
            return f"overcast-{'day' if day else 'night'}.svg"
        case 45 | 48:  # Fog and depositing rime fog
            return f"fog-{'day' if day else 'night'}.svg"
        case 51 | 53 | 55:  # Light, Moderate, Dense drizzle
            return f"partly-cloudy-{'day' if day else 'night'}-drizzle.svg"
        case 56 | 57:  # Light freezing drizzle, Dense freezing drizzle
            return "drizzle.svg"
        case 61:  # Slight rain
            return "sleet.svg"
        case 63 | 65 | 66 | 67:  # Moderate, Heavy rain, Light, dense freezing rain
            return "rain.svg"
        case 71 | 73 | 75 | 77:  # Slight, Moderate, Heavy snow fall, Snow grains
            return "snow.svg"
        case 80:  # Slight rain shower
            return "raindrop.svg"
        case 81 | 82:  # Moderate, Heavy rain shower
            return "raindrops.svg"
        case 85 | 86:  # Slight, Heavy snow shower
            return "snowflake.svg"
        case 95:  # Thunderstorm
            return f"thunderstorm-{'day' if day else 'night'}.svg"
        case 96 | 99:  # Thunderstorm with slight, heavy hail
            return f"thunderstorm-{'day' if day else 'night'}-rain.svg"
        case _:
            return "not-available.svg"


def description(weather_code: int):
    match weather_code:
        case 0:  # Clear sky
            return "Clear sky"
        case 1:  # mainly clear
            return "Mainly clear"
        case 2:  # Partly cloudy
            return "Partly cloudy"
        case 3:  # overcast
            return "Overcast"
        case 45 | 48:  # Fog and depositing rime fog
            return "Fog"
        case 51:
            return "Light drizzle"
        case 53:
            return "Moderate drizzle"
        case 55:
            return "Dense drizzle"
        case 56:
            return "Light freezing drizzle"
        case 57:
            return "Dense freezing drizzle"
        case 61:
            return "Slight rain"
        case 63:
            return "Moderate rain"
        case 65:
            return "Heavy rain"
        case 66:
            return "Light freezing rain"
        case 67:
            return "Dense freezing rain"
        case 71:
            return "Slight snow fall"
        case 73:
            return "Moderate snow fall"
        case 75:
            return "Heavy snow fall"
        case 77:
            return "Snow grains"
        case 80:
            return "Slight rain shower"
        case 81:
            return "Moderate rain shower"
        case 82:
            return "Heavy rain shower"
        case 85:
            return "Slight snow shower"
        case 86:
            return "Heavy snow shower"
        case 95:
            return "Thunderstorm"
        case 96:
            return "Thunderstorm with slight hail"
        case 99:
            return "Thunderstorm with heavy hail"
        case _:
            return "Not available"


def get_weather_data():
    r = requests.get(URL)
    data = r.json()
    temp = round(int(data["hourly"]["temperature_2m"][int(HH)]))
    windspeed = round(int(data["hourly"]["windspeed_10m"][int(HH)]))
    weather_code = data["daily"]["weathercode"][0]

    SUNRISE = data["daily"]["sunrise"][0]
    SUNSET = data["daily"]["sunset"][0]

    day = is_day(SUNRISE, SUNSET)
    icon = find_icon(weather_code, windspeed, day)

    return {
        "temperature": temp,
        "windspeed": windspeed,
        "description": description(weather_code),
        "icon": icon,
    }


if __name__ == "__main__":
    data = get_weather_data()

    print(json.dumps(data))
