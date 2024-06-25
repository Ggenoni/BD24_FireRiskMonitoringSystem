
docker-compose down --remove-orphans
docker-compose up --build


   per vedere tutti i container anche chiusi
---
LOGS
docker-compose logs -f data_fetcher
POWERSHELL DEL CONTAINER
docker run -it bdproject-mqtt-data_fetcher /bin/sh


Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

How to subscribe to topic from terminal, to check if MQTT message are send correctly:
   ```powershell
   #Accedi al container Mosquitto
   docker exec -it bdproject-mqtt-mosquitto /bin/sh

   # Isctiviti al topic
   mosquitto_sub -h localhost -t "city/select"
   mosquitto_sub -h localhost -t "city/data_raw"
   mosquitto_sub -h localhost -t "city/data_filtered"
   mosquitto_sub -h localhost -t "city/synthetic_data"
```

HOW TO ACCESS TO MONGODB
1. Accesso al Container MongoDB
docker exec -it bdproject-mqtt-mongo-1 mongosh
2. Controllo dei Dati
show dbs
3. Seleziona il Database: Supponiamo che il database si chiami data_db:
use data_db OR use weather_db
4. Mostra le Collezioni Disponibili:
show collections
5. Visualizza i Dati in una Collezione: Supponiamo che la collezione si chiami data_raw:
db.data_raw.find().pretty() OR  db.weather_data.find().pretty() 


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
We now, as students is is not always easy to navigate the word of Big Data. You may encounter some issues running this project, but we have your back covered. Here there are some helpful tips to chek if everything is running correclty, step by step. Do not desperate: one day wou will be able do code a system like this, maybe even better!

