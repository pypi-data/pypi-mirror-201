import json
import ast
import logging
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from confluent_kafka import Consumer, KafkaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col, window, from_json, current_timestamp
from pyspark.sql.types import StringType, StructType, StructField, TimestampType, IntegerType
import certifi

class create_stream_source:
    def __init__(self, kafka_connection, mongo_connection=None, time_aggregation_params=None):
        self.kafka_connection = kafka_connection
        self.mongo_connection = mongo_connection or {
            'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
            'database': 'kafkastream',
            'rawcollection': 'rawdata',
            'collection': 'sparkaggregate'
        }
        self.time_aggregation_params = time_aggregation_params

    def is_epoch(self, timestamp):
        try:
            datetime.fromtimestamp(int(timestamp))
            return True
        except ValueError:
            return False

    def process_change_event(self, change, aggregated_data_collection, spark, schema):
        document = change["fullDocument"]
        df = spark.createDataFrame([document], schema)
        aggregated_data = df \
            .groupBy(
                window("timestamp", "1 day"),
                "deviceid"
            ) \
            .agg(
                count("email").alias("email_count"),
                count("name").alias("name_count")
            )
        aggregated_data_dict = aggregated_data.collect()[0].asDict()
        try:
            json_aggregated_data = json.dumps(aggregated_data_dict)
        except Exception as e:
            logging.error("Error serializing aggregated data as JSON: %s", e)
            json_aggregated_data = None
        if json_aggregated_data is not None:
            aggregated_data_collection.update_one(
                {"window": aggregated_data_dict["window"], "deviceid": aggregated_data_dict["deviceid"]},
                {"$set": {"aggregated_data": json_aggregated_data}},
                upsert=True
            )
        else:
            logging.error("Serialized aggregated data is None, skipping update")

    def run(self):
        schema = StructType([
            StructField("timestamp", TimestampType(), True),
            StructField("name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("deviceid", IntegerType(), True)
        ])

        spark = SparkSession.builder \
            .appName("IncrementalAggregation") \
            .master("local[*]") \
            .getOrCreate()

        mongo_client = MongoClient(self.mongo_connection['uri'], server_api=ServerApi('1'), tlsCAFile=certifi.where())
        mongo_db = mongo_client[self.mongo_connection['database']]
        raw_data_collection = mongo_db[self.mongo_connection['rawcollection']]
        aggregated_data_collection = mongo_db[self.mongo_connection['collection']]

        change_stream = raw_data_collection.watch(full_document='updateLookup')

        consumer = Consumer(self.kafka_connection)
        kafka_topic = "fake-data"
        consumer.subscribe([kafka_topic])

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
            else:
                message_value = ast.literal_eval(msg.value().decode("utf-8"))
                if self.is_epoch(message_value.get("timestamp")):
                    if self.is_epoch(message_value.get("timestamp")):
                        message_value["timestamp"] = datetime.fromtimestamp(int(message_value["timestamp"]))
                    else:
                        message_value["timestamp"] = datetime.now()

                    raw_data_collection.insert_one(message_value)

                for change in change_stream:
                    self.process_change_event(change, aggregated_data_collection, spark, schema)
                    change_stream.close()
                    change_stream = raw_data_collection.watch(full_document='updateLookup')

if __name__ == "__main__":
    kafka_conn = {
        "bootstrap.servers": "your-bootstrap-server",
        "group.id": "your-group-id",
        "auto.offset.reset": "earliest"
    }
    featurizerai = create_stream_source(kafka_conn)
    featurizerai.run()
