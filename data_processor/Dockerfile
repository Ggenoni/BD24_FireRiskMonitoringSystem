FROM python:3.9-slim

RUN apt-get update && apt-get install -y iputils-ping mosquitto-clients
RUN apt-get update && apt-get install -y netcat-openbsd

COPY ../common /app/common
COPY ../fwi_calculator.py /app/
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "data_processor.py"]
