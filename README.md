
docker-compose down --remove-orphans
docker-compose up --build


   per vedere tutti i container anche chiusi
---




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
docker exec -it bdproject-mqtt-mongo-1 mongosh
```
2. Check the Databases
```sh
show dbs
```
3. Select the Database: Let's assume the database is called data_db:
```sh
use data_db
# OR
use weather_db
```
4. Show Available Collections:
```sh
show collections
```
5. View Data in a Collection: Let's assume the collection is called data_raw:
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