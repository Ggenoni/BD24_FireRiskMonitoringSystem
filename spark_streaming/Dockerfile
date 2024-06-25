FROM bitnami/spark:3.2.1

WORKDIR /app

COPY . /app

COPY COMUNI.json /app/COMUNI.json

USER root

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

USER 1001

ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH=$SPARK_HOME/bin:$PATH

EXPOSE 4040 6066 7077 8080 18080

CMD ["python3", "spark_streaming.py"]
