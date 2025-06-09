from pyspark.sql.types import *

course_schema = StructType([
    StructField("course_code", StringType(), False),
    StructField("name", StringType(), True),
    StructField("eng_name", StringType(), True),
])