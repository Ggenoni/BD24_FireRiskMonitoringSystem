from flask import Flask, render_template, request, jsonify
import json
import paho.mqtt.client as mqtt
import time

app = Flask(__name__)

# MQTT setup
mqtt_broker = 'mosquitto'
mqtt_topic_city = 'city/select'
mqtt_topic_data_filtered = 'city/data_filtered'
mqtt_topic_alerts = 'city/synthetic_data'  

client = mqtt.Client()
client.connect(mqtt_broker, 1883, 60)

city_data_response = {}
# Set up for 'real time' alerts
alerts_data = {}  
alerts_list = [] 
MAX_ALERTS = 5  

def on_alert_message(client, userdata, msg):
    global alerts_data, alerts_list
    try:
        alert = json.loads(msg.payload)
        print(f"Received alert payload: {alert}")  
        if 'city_name' in alert and 'fwi_level' in alert:
            city_name = alert['city_name']
            
            if city_name in alerts_data:
                alerts_list.remove(city_name)
            
            alerts_list.append(city_name)
            alerts_data[city_name] = alert
            
            if len(alerts_list) > MAX_ALERTS:
                oldest_city = alerts_list.pop(0)
                del alerts_data[oldest_city]

            print(f"Processed alert: {alert}")  
        else:
            print(f"Invalid alert format: {alert}") 
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON payload: {msg.payload}, error: {e}")

client.message_callback_add(mqtt_topic_alerts, on_alert_message)
client.subscribe(mqtt_topic_alerts)

def on_message(client, userdata, msg):
    global city_data_response
    data = json.loads(msg.payload)
    city_data_response[data['city']] = data
    print(f"Received message on {msg.topic}: {data}")

client.on_message = on_message
client.subscribe(mqtt_topic_data_filtered)
client.loop_start()

def load_json_to_dict(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

# USAGE
json_file_path = 'COMUNI.json'  
italy_data = load_json_to_dict(json_file_path)

@app.route('/')
def index():
    regions = list(italy_data.keys())
    alerts = get_alerts_from_mqtt()  
    return render_template('index.html', regions=regions, alerts=alerts)

def get_alerts_from_mqtt():
    significant_alerts = [alert for alert in alerts_data.values() if alert['fwi_level'] in ["Extreme", "Very-High", "High"]]
    significant_alerts.sort(key=lambda x: ["Extreme", "Very-High", "High", "Moderate"].index(x["fwi_level"]))
    print(f"Filtered alerts: {significant_alerts}")  
    return significant_alerts

@app.route('/provinces/<region>')
def provinces(region):
    provinces = list(italy_data.get(region, {}).keys())
    return jsonify(provinces)

@app.route('/municipalities/<region>/<province>')
def municipalities(region, province):
    province_data = italy_data.get(region, {}).get(province, [])
    municipalities_names = sorted({city_info['nome'] for city_info in province_data})
    return jsonify(municipalities_names)

@app.route('/city-data', methods=['POST'])
def city_data():
    global city_data_response
    city = request.form.get('municipality')
    client.publish(mqtt_topic_city, city)
    print(f"Published city {city} to MQTT")

    start_time = time.time()
    timeout = 30
    while city not in city_data_response:
        if time.time() - start_time > timeout:
            return jsonify({"message": "Timeout waiting for city data", "city": city})

    data = city_data_response.pop(city)
    print(f"Received data for city {city}: {data}")
    return render_template('city_data.html', city=city, current_data=data['current_data'], 
                           forecast_data=data['forecast_data'], forecast_time=data['forecast_time'],
                           fwi_current=data['fwi_current'], fwi_forecast=data['fwi_forecast'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
