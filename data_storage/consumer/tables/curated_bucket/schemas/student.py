from pyspark.sql.types import *

student_schema = StructType([
    StructField("student_code", IntegerType(), False),
    StructField("class_code", StringType(), False),
])