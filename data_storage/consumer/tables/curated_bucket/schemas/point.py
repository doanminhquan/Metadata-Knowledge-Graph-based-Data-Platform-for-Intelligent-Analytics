from pyspark.sql.types import *

point_schema = StructType([
    StructField("student_code", IntegerType(), False),
    StructField("course_section_code", StringType(), False),
    StructField("term_code", StringType(), False),
    StructField("point_4", DoubleType(), True),
    StructField("point_10", DoubleType(), True),
])