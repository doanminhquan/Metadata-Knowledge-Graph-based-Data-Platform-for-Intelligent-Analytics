from pyspark.sql.types import *

enrollment_schema = StructType([
    StructField("student_code", IntegerType(), False),
    StructField("course_group_code", StringType(), False),
])