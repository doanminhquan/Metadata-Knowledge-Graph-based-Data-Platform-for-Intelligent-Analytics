from pyspark.sql.types import *

term_schema = StructType([
    StructField("term_code", StringType(), False),
    StructField("term_name", StringType(), True),
])