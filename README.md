# Usage:

* First train the anomaly detection model, run the file:

```bash
model/train.py
```
* run kafka by docker
```
docker-compose up -d 
```

* ssh to the docker container
```
docker exec -it broker sh
```

* Create the required topics

```
kafka-topics --bootstrap-server broker:9092 --topic transactions --create --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server broker:9092 --topic anomalies --create --partitions 3 --replication-factor 1
```

* Start the producer, run the file

```bash
python3 streaming/producer.py
```

* Start the anomalies detector, run the file

```
python3 streaming/anomalies_detector.py
```

* Send alerts to file alerts.txt,

```
python3 streaming/bot_alerts.py
```

* Tail the results

```
tail -f 100 alerts.txt
```