from pyspark.sql.types import *

course_group_detail_schema = StructType([
    StructField("course_group_code", StringType(), False),
    StructField("room_code", IntegerType(), True),
    StructField("session_start", IntegerType(), True),
    StructField("session_end", IntegerType(), True),
    StructField("weekday", IntegerType(), True),
    StructField("staff_code", StringType(), True)
])