# --- Open cmt line bellow if run by cmd: python *.py
# import sys  # nopep8
# sys.path.append(".")  # nopep8
# ----

print("ok1")
import json
import os
from joblib import load
import logging
from multiprocessing import Process
print("ok2")
import numpy as np
print("ok3")
from utils import create_producer, create_consumer
from settings import TRANSACTIONS_TOPIC, TRANSACTIONS_CONSUMER_GROUP, ANOMALIES_TOPIC, NUM_PARTITIONS
print("ok4")
model_path = os.path.abspath('../kafkaml-anomaly-detection/model/isolation_forest.joblib')
print("ok5")

def detect():
    consumer = create_consumer(topic=TRANSACTIONS_TOPIC, group_id=TRANSACTIONS_CONSUMER_GROUP)

    producer = create_producer()

    clf = load(model_path)

    while True:
        message = consumer.poll(timeout=50)
        print(message)
        if message is None:
            continue
        if message.error():
            logging.error("Consumer error: {}".format(message.error()))
            continue

        # Message that came from producer
        record = json.loads(message.value().decode('utf-8'))
        data = record["data"]

        prediction = clf.predict(data)

        # If an anomaly comes in, send it to anomalies topic
        if prediction[0] == -1:
            score = clf.score_samples(data)
            record["score"] = np.round(score, 3).tolist()
            
            _id = str(record["id"])
            record = json.dumps(record).encode("utf-8")
            print(record)
            producer.produce(topic=ANOMALIES_TOPIC,
                             value=record)
            producer.flush()

        # consumer.commit() # Uncomment to process all messages, not just new ones

    consumer.close()
print("ok6")

# One consumer per partition
if __name__ == "__main__":
    detect()
    # for _ in range(NUM_PARTITIONS):
    #     p = Process(target=detect)
    #     p.start()
