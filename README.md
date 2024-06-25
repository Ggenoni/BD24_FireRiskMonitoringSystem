
docker-compose down --remove-orphans
docker-compose up --build

### Fire Risk Monitoring System

This repository contains the Fire Weather Index (FWI) System developed by Group 12. The project aims to calculate the Fire Weather Index (FWI) using real-time weather data for all Italian municipalities. The system provides the FWI for current weather conditions as well as a 5-day forecast.

### Abstract

The project predicts the Fire Weather Index (FWI) for various cities using real-time weather data and forecasts. The system consists of four main components:
- **User Interface (UI)**
- **Data Fetcher**
- **Data Processor**
- **Spark Streaming Processor**

These components communicate through an MQTT message queue.

### Technologies Used

- **Apache Spark**
- **MongoDB**
- **Docker + Docker Compose**
- **Flask** (Python framework)
- **Paho-MQTT**
- **PyYAML**
- **NumPy**
- **Requests**

### Project Structure

The repository is organized as follows:

```
.
├── data_fetcher
│   ├── Dockerfile
│   ├── data_fetcher.py
│   ├── requirements.txt
├── data_processor
│   ├── Dockerfile
│   ├── data_processor.py
│   ├── requirements.txt
│   └── fwi_calculator.py
├── spark_streaming
│   ├── Dockerfile
│   ├── spark_streaming.py
│   ├── requirements.txt
│   └── fwi_calculator.py
├── UserInterface
│   ├── Dockerfile
│   ├── ui_flask.py
│   ├── requirements.txt
│   ├── COMUNI.json
│   ├── templates
│   │   └── ...
│   ├── static
│       └── ...
├── mongo
│   └── ...
├── mosquitto
│   └── ...
├── docker-compose.yml
├── config.yaml
├── requirements.txt
└── README.md
```

### Setup and Configuration

#### Configuration File

The configuration file `config.yaml` includes necessary parameters for API keys from [OpenWeather](https://openweathermap.org/api). Ensure it is correctly set up before running the application.

If you are the professors of the course BDT, check the email with the deliver of the project, the API for you is there!

#### Docker Setup

The project uses Docker Compose to manage and run services. It includes the Docker Compose file `docker-compose.yml` which sets up Kafka, Zookeeper, MongoDB, Mongo Express, and Apache Spark.

Before running these, ensure the `config/config.yaml` has the correct environment settings for Docker.

### How to Run

1. **Start Services**:
    ```sh
    docker-compose up
    ```

2. **Start User Interface**:
    ```sh
    python3 UserInterface/ui_flask.py
    ```

Access the user interface at `http://localhost:5000`.

### Components Description

#### User Interface (UI)

- **Files**:
  - `ui_flask.py`: Main file to run the UI component.
  - `templates`: HTML templates for the UI.
  - `static`: Static files like CSS and JS.
  - `COMUNI.json`: Contains city data.

#### Data Fetcher

- **Files**:
  - `data_fetcher.py`: Fetches real-time weather and forecast data, publishes to MQTT.
  - `requirements.txt`: Dependencies for data fetcher.

The Data Fetcher subscribes to the `city/select` topic, fetches current and forecasted weather data for the specified city, and publishes the raw data to the `city/data_raw` topic.

#### Data Processor

- **Files**:
  - `data_processor.py`: Processes raw data, calculates Fire Weather Index (FWI), stores in MongoDB, and publishes to MQTT.
  - `fwi_calculator.py`: Contains functions to calculate FWI.
  - `requirements.txt`: Dependencies for data processor.

The Data Processor subscribes to the `city/data_raw` topic, processes the data to compute the FWI, and publishes the processed data to the `city/data_filtered` topic.

#### Spark Streaming

- **Files**:
  - `spark_streaming.py`: Uses Spark for streaming data processing.
  - `fwi_calculator.py`: Contains functions to calculate FWI.
  - `requirements.txt`: Dependencies for Spark streaming.

The Spark Streaming component processes the streaming data to provide real-time updates and predictions.

### To Be Implemented

- Improvement of the fire weather prediction model using historical weather data.
- Switch computation to Apache Spark for better management of high volume requests.
- Add error control and monitoring for the pipeline to handle failures and recover from checkpoints.

### Dependencies

- **Docker** v24.0.2
- **Docker Compose** v2.18.1
- **Python** v3.11.0
- **Flask** v2.3.2

Ensure all dependencies are installed and correctly set up to run the project successfully.

### Contribution

Contributions are welcome. Please create a pull request with a detailed description of your changes.

---

This README provides a comprehensive guide to understanding, setting up, and running the Forest Fire Weather Index Prediction System. For further details, refer to the specific files and configurations in the repository.


running on http://127.0.0.1:5000

### To Be Implemented Yet

+ 
+ 
+

---
### Authors
This project was created by group 12, consisting of:
 - Agnese Cervino - [@AgneCer](https://github.com/AgneCer)
 - Alessandra Gandini - [@alegandini](https://github.com/alegandini)
 - Gaudenzia Genoni - [@Ggenoni](https://github.com/Ggenoni)



---
### Need some help?
If you are still a student, like us, it is not always easy to navigate the world of Big Data. You may encounter some issues running this project, but we've got your back. Here are some helpful tips to check if everything is running correctly, step by step. Do not despair: one day you will be able to code a system like this, maybe even better!

##### IS MQTT WORKING?

With the following code, you can subscribe to topics, send messages, and check if everything is working.

Access to container Mosquitto
```
   docker exec -it [name_of_container_mosquitto] /bin/sh
```
Subscribe to the topic you want to check
```
   mosquitto_sub -h localhost -t "city/select"
   mosquitto_sub -h localhost -t "city/data_raw"
   mosquitto_sub -h localhost -t "city/data_filtered"
   mosquitto_sub -h localhost -t "city/synthetic_data"
```

##### HOW DO I ACCESS MONGODB?

1. Access the MongoDB Container
```sh
docker exec -it [name_of_container_mongo] mongosh
```
2. Check the Databases
```sh
show dbs
```
3. Select the Database: 
```sh
use data_db
# OR
use weather_db
```
4. Show Available Collections:
```sh
show collections
```
5. View Data in a Collection: 
```sh
db.data_raw.find().pretty()
# OR
db.weather_data.find().pretty()
```

##### ARE CONTAINERS WORKING?

Check the status of containers:
```
docker ps -a
```
Check the logs of a specific container
```
docker-compose logs -f [container_name]
```


##### IS THE CODE INSIDE CONTAINER WORKING?

Access to the powershell of the container
```
docker run -it [container_name] /bin/sh
```
Run the code
```
python [program].py
```