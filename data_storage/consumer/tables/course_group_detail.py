import json
from confluent_kafka import Consumer
from raw_bucket.write_to_raw_bucket import write_raw_bucket
from pyspark.sql.types import *


conf = {
    'bootstrap.servers': 'localhost:9098', 
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest' 
}

consumer = Consumer(conf)
consumer.subscribe(['dbserver1.school.course_group_detail']) 

course_group_detail_payload_schema = StructType([
    StructField("before", StructType([
        StructField("course_group_code", StringType(), False),
        StructField("room_code", IntegerType(), False),
        StructField("session_start", IntegerType(), False),
        StructField("session_end", IntegerType(), True),
        StructField("weekday", IntegerType(), False),
        StructField("staff_code", StringType(), True),
    ]), True),

    StructField("after", StructType([
        StructField("course_group_code", StringType(), False),
        StructField("room_code", IntegerType(), False),
        StructField("session_start", IntegerType(), False),
        StructField("session_end", IntegerType(), True),
        StructField("weekday", IntegerType(), False),
        StructField("staff_code", StringType(), True),
    ]), True),

    StructField("source", StructType([
        StructField("version", StringType(), False),
        StructField("connector", StringType(), False),
        StructField("name", StringType(), False),
        StructField("ts_ms", LongType(), False),
        StructField("snapshot", StringType(), True),
        StructField("db", StringType(), False),
        StructField("sequence", StringType(), True),
        StructField("ts_us", LongType(), True),
        StructField("ts_ns", LongType(), True),
        StructField("table", StringType(), True),
        StructField("server_id", LongType(), False),
        StructField("gtid", StringType(), True),
        StructField("file", StringType(), False),
        StructField("pos", LongType(), False),
        StructField("row", IntegerType(), False),
        StructField("thread", LongType(), True),
        StructField("query", StringType(), True),
    ]), False),

    StructField("transaction", StructType([
        StructField("id", StringType(), False),
        StructField("total_order", LongType(), False),
        StructField("data_collection_order", LongType(), False),
    ]), True),

    StructField("op", StringType(), False),
    StructField("ts_ms", LongType(), True),
    StructField("ts_us", LongType(), True),
    StructField("ts_ns", LongType(), True),
])

full_schema = StructType([
    StructField("schema", MapType(StringType(), StringType()), True),  
    StructField("payload", course_group_detail_payload_schema, True)
])

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
                write_raw_bucket(data=json_data, bucket="raw_bucket", status="unprocessed", database="school", table="course_group_detail", schema=full_schema)
        except json.JSONDecodeError:
            print(f"Received non-JSON message: {message_value}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
