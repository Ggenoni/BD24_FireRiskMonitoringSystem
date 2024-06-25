import numpy as np
from datetime import datetime

def calculate_ffmc(temperature, relative_humidity, rain):
    ffmc0 = 85.0
    mo = 147.2 * (101.0 - ffmc0) / (59.5 + ffmc0)

    if rain > 0.5:
        rf = rain - 0.5
        mo += 42.5 * rf * np.exp(-100.0 / (251.0 - mo))
        mo = min(mo, 250.0)

    ed = 0.942 * (relative_humidity**0.679) + (11.0 * np.exp((relative_humidity - 100.0) / 10.0)) + 0.18 * (21.1 - temperature) * (1.0 - 1.0 / np.exp(0.115 * relative_humidity))
    if mo < ed:
        ew = 0.618 * (relative_humidity**0.753) + (10.0 * np.exp((relative_humidity - 100.0) / 10.0)) + 0.18 * (21.1 - temperature) * (1.0 - 1.0 / np.exp(0.115 * relative_humidity))
        mo = ew + (mo - ew) / 10.0

    ffmc = (59.5 * (250.0 - mo)) / (147.2 + mo)
    ffmc = min(max(ffmc, 0.0), 101.0)

    return ffmc

def calculate_dmc(temperature, relative_humidity, rain, month):
    el = 0.92 * rain - 1.27
    if el < 0:
        el = 0
    pe = 0.484 * np.exp(0.191 * temperature - 0.0042 * relative_humidity) * el
    if pe < 0:
        pe = 0

    dmc = pe + 0.923 * temperature + 0.374 * (1 - 0.3 * relative_humidity)
    return dmc

def calculate_dc(temperature, rain, month):
    t = temperature + 2.1
    el = rain - 1.5
    if el < 0:
        el = 0
    dc = el * 0.36 * np.exp(0.069 * t)
    return dc

def calculate_isi(wind_speed, ffmc):
    isi = 0.208 * np.exp(0.05039 * wind_speed)
    return isi

def calculate_bui(dmc, dc):
    bui = dmc + dc
    return bui

def calculate_fwi_from_subindices(isi, bui):
    fwi = isi * bui
    return fwi

def evaluate_fwi(fwi):
    if fwi < 5.2:
        return "Low"
    elif 5.2 <= fwi < 12.2:
        return "Moderate"
    elif 12.2 <= fwi < 21.3:
        return "High"
    elif 21.3 <= fwi < 38:
        return "Very-High"
    else:
        return "Extreme"

def total_fwi(temperature, relative_humidity, rain, wind_speed):
    month = datetime.now().month  
    wind_speed = wind_speed * 3.6  
    ffmc = calculate_ffmc(temperature, relative_humidity, rain)
    dmc = calculate_dmc(temperature, relative_humidity, rain, month)
    dc = calculate_dc(temperature, rain, month)
    isi = calculate_isi(wind_speed, ffmc)
    bui = calculate_bui(dmc, dc)
    fwi = calculate_fwi_from_subindices(isi, bui)
    risk_level = evaluate_fwi(fwi)
    return fwi, risk_level

