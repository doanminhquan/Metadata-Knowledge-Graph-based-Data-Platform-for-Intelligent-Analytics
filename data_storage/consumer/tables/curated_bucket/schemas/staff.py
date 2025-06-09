from pyspark.sql.types import *

staff_schema = StructType([
    StructField("staff_code", StringType(), False),
    StructField("staff_name", StringType(), True),
])