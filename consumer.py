
from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'sensor_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

MONGODB_URI = "mongodb+srv://pravallikachivukula173:mongodblessons@cluster1.cq5ypgv.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)
db = client.database_sc
collection = db.sensor_readings

print("Kafka consumer started. Waiting for messages...")

for message in consumer:
    data = message.value
    collection.insert_one(data)
    print(f"Inserted into MongoDB: {data}")

