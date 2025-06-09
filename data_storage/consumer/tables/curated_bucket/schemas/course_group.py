from pyspark.sql.types import *

course_group_schema = StructType([
    StructField("course_group_code", StringType(), False),
    StructField("course_section_code", StringType(), True),
    StructField("student_amount", IntegerType(), True),
    StructField("type", StringType(), True),
    StructField("group_order", IntegerType(), True),
])