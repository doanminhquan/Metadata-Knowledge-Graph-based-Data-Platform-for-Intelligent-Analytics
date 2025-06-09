from pyspark.sql.types import *

course_section_schema = StructType([
    StructField("course_section_code", StringType(), True),
    StructField("course_code", StringType(), True),
    StructField("term_code", StringType(), True),
])