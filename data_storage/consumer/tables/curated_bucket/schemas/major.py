from pyspark.sql.types import *

major_schema = StructType([
    StructField("major_code", StringType(), False),
    StructField("name", StringType(), True),
])