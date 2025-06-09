from confluent_kafka import Consumer, KafkaException

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9098',  
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest' 
}

# Create consumer
consumer = Consumer(conf)
consumer.subscribe(['schema-changes.school']) 

try:
    while True:
        msg = consumer.poll(1.0)  

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        print(f"Received message: {msg.value().decode('utf-8', errors='ignore')}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
