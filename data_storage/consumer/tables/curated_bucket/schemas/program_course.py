from pyspark.sql.types import *

program_course_schema = StructType([
    StructField("program_code", StringType(), False),
    StructField("course_code", StringType(), False),
    StructField("type", StringType(), False),
])