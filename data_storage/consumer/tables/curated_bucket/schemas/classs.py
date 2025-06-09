from pyspark.sql.types import *

class_schema = StructType([
    StructField("class_code", StringType(), False),
    StructField("program_code", StringType(), True),
    StructField("year_start", IntegerType(), True),
    StructField("name", StringType(), True),
])