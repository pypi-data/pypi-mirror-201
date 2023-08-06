from ..src.featurizerai.features.createFeatureViewFromKafKa import create_stream_source

def main():
    kafka_connection = {
        "bootstrap.servers": "buraks-air.lan:9092",
        "group.id": "your-group-id",
        "auto.offset.reset": "earliest"
    }

    # Optional: Provide custom MongoDB connection settings
    mongo_connection = {
        'uri': "mongodb+srv://admin:6lHqq9LqgwDlninK@cluster0.aqtcyq2.mongodb.net/?retryWrites=true&w=majority",
        'database': 'kafkastream',
        'rawcollection': 'rawdata',
        'collection': 'sparkaggregate'
    }

    # Initialize the FeaturizerAI SDK with the Kafka and Mongo connections
    featurizer_ai = create_stream_source(kafka_connection, mongo_connection)

    # Run the FeaturizerAI processing
    featurizer_ai.run()

if __name__ == "__main__":
    main()
