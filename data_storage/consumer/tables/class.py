import json
from confluent_kafka import Consumer
from raw_bucket.write_to_raw_bucket import write_raw_bucket
from pyspark.sql.types import *
import json
import time

conf = {
    'bootstrap.servers': 'localhost:9098', 
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest' 
}

consumer = Consumer(conf)
consumer.subscribe(['dbserver1.school.class']) 


total_time = 0.0
message_count = 0


class_payload_schema = StructType([
    StructField("before", StructType([
        StructField("class_code", StringType(), False),
        StructField("program_code", StringType(), True),
        StructField("year_start", IntegerType(), True),
        StructField("name", StringType(), True),
    ]), True),

    StructField("after", StructType([
        StructField("class_code", StringType(), False),
        StructField("program_code", StringType(), True),
        StructField("year_start", IntegerType(), True),
        StructField("name", StringType(), True),
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
    StructField("payload", class_payload_schema, True)
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
            #    start_time = time.time()
                message_value = msg.value().decode('utf-8', errors='ignore')
                json_data = json.loads(message_value)
                write_raw_bucket(data=json_data, bucket="raw_bucket", status="unprocessed", database="school", table="class", schema=full_schema)
            #    end_time = time.time()
            #    elapsed_time = end_time - start_time
            #    total_time += elapsed_time
            #    message_count += 1
            #    with open("/dis/nhap/message_count.txt", "a") as f:
            #        f.write(str(json_data) + "\n")
            #    print(f"Processing time: {elapsed_time:.4f} seconds")
            #    print(f"Total processing time: {total_time:.4f} seconds for {message_count} messages")
        except json.JSONDecodeError:
            print(f"Received non-JSON message: {message_value}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
