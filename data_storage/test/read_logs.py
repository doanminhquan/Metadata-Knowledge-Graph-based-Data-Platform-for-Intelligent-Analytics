from pyspark.sql import SparkSession
import json

def read_logs(bucket, database, table):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("ReadFromMinIO") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9008") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

    # Read Parquet file from MinIO
    path = f"s3a://warehouse/raw_data/unprocessed/{database}/{table}"
    df = spark.read.parquet(path)

    # Extract only the 'payload' field if it exists
    if "payload" in df.columns:
        df = df.select("payload")

    # Convert DataFrame to JSON and parse it
    json_data = df.toJSON().collect()

    # Stop Spark
    spark.stop()

    # Iterate through each record
    for item in json_data:
        record = json.loads(item)  # Convert string to dictionary
        payload = record.get("payload", {})  # Extract payload

        # Extract "after" data if available
        after_data = payload.get("after", {})
        if after_data:
            print("New Student Record:")
            for key, value in after_data.items():
                print(f"{key}: {value}")
            print("-" * 30)  # Separator for better readability
        else:
            print("No new student data found.")

# Example Usage
read_logs("warehouse", "school", "students")
