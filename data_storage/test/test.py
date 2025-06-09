from confluent_kafka.admin import AdminClient

# Kafka broker address
bootstrap_servers = "localhost:9098"  # Change this to your broker address

# Create an admin client
admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})

# Fetch the list of topics
topic_metadata = admin_client.list_topics(timeout=10)

# Print topic names
print("Kafka Topics:")
for topic in topic_metadata.topics:
    print(topic)
