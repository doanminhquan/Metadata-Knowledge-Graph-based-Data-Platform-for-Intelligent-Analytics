from pyspark.sql import SparkSession
import json
from pyspark.sql.functions import col
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

def write_raw_bucket(data, bucket, status, database, table, schema):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("WriteToMinIO") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9008") \
        .config("spark.hadoop.fs.s3a.access.key", "admin") \
        .config("spark.hadoop.fs.s3a.secret.key", "password") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.jars.packages","io.acryl:acryl-spark-lineage:0.2.17") \
        .config("spark.extraListeners","datahub.spark.DatahubSparkListener") \
        .config("spark.datahub.rest.server","http://localhost:22691") \
        .getOrCreate()
        
    # Create DataFrame
    df = spark.createDataFrame([data], schema=schema)

    # if "payload.after.avg_score" in df.columns:
    #     df = df.withColumn("avg_score", col("payload.after.avg_score").cast("decimal(5,2)"))
    # df = spark.read.json(spark.sparkContext.parallelize([json.dumps(data)]))

    # Write DataFrame to MinIO in Parquet format
    df.write.mode("append").parquet(f"s3a://warehouse/{bucket}/{status}/{database}/{table}")

    print("Data written to MinIO successfully!")

    # Stop Spark
    spark.stop()




# spark = SparkSession.builder \
#     .appName("WriteToMinIO") \
#     .master("spark://uet-data:7077") \
#     .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9008") \
#     .config("spark.hadoop.fs.s3a.access.key", "admin") \
#     .config("spark.hadoop.fs.s3a.secret.key", "password") \
#     .config("spark.hadoop.fs.s3a.path.style.access", "true") \
#     .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
#     .getOrCreate()