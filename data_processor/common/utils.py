from datetime import datetime, timedelta
from fwi_calculator import total_fwi
import json

def fetch_current_useful(current_weather):
    temp = current_weather['main']['temp']  # °C
    hum = current_weather['main']['humidity']  # %
    win = current_weather['wind']['speed']  # m/s
    try:
        rai = current_weather['rain']['1h']  # mm
    except KeyError:
        rai = 0
    
    return {
        'temperature': temp,
        'humidity': hum,
        'wind_speed': win,
        'rain': rai
    }

def fetch_forecast_useful(forecast_data):
    forecast_data_filtered = []
    forecast_time = []
    for forecast in forecast_data['list']:
        tmp = []
        tmp.append(forecast['main']['temp'])  # °C
        tmp.append(forecast['main']['humidity'])  # %
        tmp.append(forecast['wind']['speed'])  # m/s
        try:
            tmp.append(round(forecast['rain']['3h'] / 3, 2))  # divided by 3 because the rain is reported in 3h
        except KeyError:
            tmp.append(0)  # °C
        forecast_data_filtered.append(tmp)
        forecast_time.append(forecast['dt_txt'])
    return forecast_data_filtered, forecast_time



# Useful for further implementation of real time alerts
'''
def get_alerts():
    alerts = []
    with open('real_time_data.json', 'r', encoding='utf-8') as file:
        real_time_data = json.load(file)
    for city_data in real_time_data:
        weather = city_data["main"]
        temp = weather["temp"]
        hum = weather["humidity"]
        rain = city_data["rain"]["1h"] if "rain" in city_data and "1h" in city_data["rain"] else 0
        wind_speed = city_data["wind"]["speed"]

        fwi_value, fwi_level = total_fwi(temp, hum, rain, wind_speed)
        if fwi_level in ["Extreme", "Very-High", "High"]:
            alerts.append({
                "name": city_data["name"],
                "fwi_level": fwi_level
            })
    alerts.sort(key=lambda x: ["Extreme", "Very-High", "High", "Moderate"].index(x["fwi_level"]))
    return alerts

'''