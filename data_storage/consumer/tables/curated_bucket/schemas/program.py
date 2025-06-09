from pyspark.sql.types import *

program_schema = StructType([
    StructField("program_code", StringType(), False),
    StructField("name", StringType(), True),
    StructField("major_code", StringType(), True),
])