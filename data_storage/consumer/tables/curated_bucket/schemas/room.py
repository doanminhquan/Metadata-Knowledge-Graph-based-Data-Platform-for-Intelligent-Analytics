from pyspark.sql.types import *

room_schema = StructType([
    StructField("room_code", IntegerType(), False),
    StructField("room_name", StringType(), True),
    StructField("capacity", IntegerType(), True),
])