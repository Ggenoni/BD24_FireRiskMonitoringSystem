from pyspark.sql import SparkSession
import paho.mqtt.client as mqtt
import json
import time
import logging
from fwi_calculator import total_fwi
import random

spark = SparkSession.builder.appName("SparkStreamingApp").getOrCreate()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker successfully")
    else:
        logger.error(f"Failed to connect to MQTT Broker, return code {rc}")

def on_publish(client, userdata, mid):
    logger.info(f"Message {mid} has been published.")

def on_log(client, userdata, level, buf):
    logger.info(f"Log: {buf}")

def process_and_publish_data():
    try:
        
        # Useful for implementing with real streaming data, but here not used
        '''
        schema = StructType([
            StructField("main", StructType([
                StructField("temp", DoubleType(), True),
                StructField("feels_like", DoubleType(), True),
                StructField("temp_min", DoubleType(), True),
                StructField("temp_max", DoubleType(), True),
                StructField("pressure", IntegerType(), True),
                StructField("humidity", DoubleType(), True),
                StructField("sea_level", IntegerType(), True),
                StructField("grnd_level", IntegerType(), True)
            ]), True),
            StructField("visibility", IntegerType(), True),
            StructField("wind", StructType([
                StructField("speed", DoubleType(), True),
                StructField("deg", IntegerType(), True),
                StructField("gust", DoubleType(), True)
            ]), True),
            StructField("rain", StructType([
                StructField("1h", DoubleType(), True)
            ]), True),
            StructField("clouds", StructType([
                StructField("all", IntegerType(), True)
            ]), True),
            StructField("weather", StructType([
                StructField("id", IntegerType(), True),
                StructField("main", StringType(), True),
                StructField("description", StringType(), True),
                StructField("icon", StringType(), True)
            ]), True),
            StructField("coord", StructType([
                StructField("lon", DoubleType(), True),
                StructField("lat", DoubleType(), True)
            ]), True),
            StructField("dt", LongType(), True),
            StructField("sys", StructType([
                StructField("type", IntegerType(), True),
                StructField("id", IntegerType(), True),
                StructField("country", StringType(), True),
                StructField("sunrise", LongType(), True),
                StructField("sunset", LongType(), True)
            ]), True),
            StructField("timezone", IntegerType(), True),
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("cod", IntegerType(), True)
        ])
        
        logger.info("Reading JSON data from /app/live_data.json")
        df = spark.read.schema(schema).json("/app/live_data.json")

        df.createOrReplaceTempView("weather_data")

        logger.info("Processing weather data")
        processed_data = spark.sql("""
            SELECT
                name,
                main.temp AS temp,
                main.humidity AS humidity,
                wind.speed AS speed,
                rain['1h'] AS rain
            FROM weather_data
        """)

        logger.info("Collecting weather data")
        weather_data = processed_data.collect()

        '''
        # Generation of synthetic data

        with open('COMUNI.json', 'r', encoding='utf-8') as file:
            comuni = json.load(file)

        for i in range (200):
            city_name = random.choice([comune['nome'] for region in comuni.values() for province in region.values() for comune in province])
            temp = random.uniform(0, 50)
            humidity = random.uniform(10, 90)
            wind_speed = random.uniform(0, 15)
            rain = round(random.uniform(0, 8), 2)


            # Calculate FWI
            try:
                fwi_value, fwi_level = total_fwi(temp, humidity, wind_speed, rain)
                
                message = {
                    "city_name": city_name,
                    "fwi_level": fwi_level
                }

                client.publish("city/synthetic_data", json.dumps(message))
            except Exception as fwi_error:
                logger.error(f"Error calculating FWI for {city_name}: {fwi_error}")

    except Exception as e:
        logger.error(f"Error processing data: {e}")

if __name__ == "__main__":
    mqtt_broker = "mosquitto"  
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_log = on_log

    client.connect(mqtt_broker, 1883, 60)
    client.loop_start()

    while True:
        process_and_publish_data()
        logger.info("Sleeping for 20 seconds")
        time.sleep(20)
