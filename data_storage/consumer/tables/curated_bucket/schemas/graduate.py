from pyspark.sql.types import *

graduate_schema = StructType([
    StructField("term_code", StringType(), True),
    StructField("rank", StringType(), True),
    StructField("program_code", StringType(), True),
    StructField("student_code", IntegerType(), True),
    StructField("avg_score", DoubleType(), True),
])