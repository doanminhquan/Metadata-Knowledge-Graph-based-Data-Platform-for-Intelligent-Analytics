


import json
from confluent_kafka import Consumer
from raw_bucket.write_to_raw_bucket import write_raw_bucket
from pyspark.sql.types import *

conf = {
    'bootstrap.servers': 'localhost:9098', 
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest' 
}

student_payload_schema = StructType([
    StructField("before", StructType([
        StructField("student_code", IntegerType(), True),
        StructField("class_code", StringType(), True),
    ]), True),

    StructField("after", StructType([
        StructField("student_code", IntegerType(), True),
        StructField("class_code", StringType(), True),
    ]), True),

    StructField("source", StructType([
        StructField("version", StringType(), True),
        StructField("connector", StringType(), True),
        StructField("name", StringType(), True),
        StructField("ts_ms", LongType(), True),
        StructField("snapshot", StringType(), True),
        StructField("db", StringType(), True),
        StructField("sequence", StringType(), True),
        StructField("ts_us", LongType(), True),
        StructField("ts_ns", LongType(), True),
        StructField("table", StringType(), True),
        StructField("server_id", LongType(), True),
        StructField("gtid", StringType(), True),
        StructField("file", StringType(), True),
        StructField("pos", LongType(), True),
        StructField("row", IntegerType(), True),
        StructField("thread", LongType(), True),
        StructField("query", StringType(), True),
    ]), True),

    StructField("transaction", StructType([
        StructField("id", StringType(), True),
        StructField("total_order", LongType(), True),
        StructField("data_collection_order", LongType(), True),
    ]), True),

    StructField("op", StringType(), True),
    StructField("ts_ms", LongType(), True),
    StructField("ts_us", LongType(), True),
    StructField("ts_ns", LongType(), True),
])

full_schema = StructType([
    StructField("schema", MapType(StringType(), StringType()), True), 
    StructField("payload", student_payload_schema, True)
])

consumer = Consumer(conf)
consumer.subscribe(['dbserver1.school.student']) 

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        try:
            if msg.value():
                message_value = msg.value().decode('utf-8', errors='ignore')
                json_data = json.loads(message_value)
                write_raw_bucket(data=json_data, bucket="raw_bucket", status="unprocessed", database="school", table="student", schema=full_schema)
        except json.JSONDecodeError:
            print(f"Received non-JSON message: {message_value}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()