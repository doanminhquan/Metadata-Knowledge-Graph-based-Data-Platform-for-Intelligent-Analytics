from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark.sql.functions import countDistinct
from pyspark.sql.functions import avg, col, unbase64, udf, round
from pyspark.sql.types import DoubleType
from pyspark.sql import Row
import struct   
import base64

# Order:
#   Spark extra configs
#   Hudi
#   MinIO/S3
#   DataHub
def configure_spark_with_hudi_minio():
    spark = (SparkSession.builder
        .appName("Spark: Write to Gold Bucket")
        .config("spark.jars.packages", "org.apache.hudi:hudi-spark3-bundle_2.12:0.15.0,io.acryl:acryl-spark-lineage:0.2.17,org.apache.hudi:hudi-utilities-slim-bundle_2.12:1.0.1,org.apache.hudi:hudi-datahub-sync-bundle:1.0.2")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .config("spark.default.parallelism", "100")
        .config("spark.sql.shuffle.partitions", "100")
        .config("spark.sql.hive.metastore.version", "2.3.9")
        .config("spark.sql.warehouse.dir", "s3a://warehouse/spark-warehouse")
        .config("spark.sql.hive.convertMetastoreParquet", "false")
        .config("spark.local.dir", "/data/spark/tmp")

        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog")
        .config("spark.kryo.registrator", "org.apache.spark.HoodieSparkKryoRegistrar")

        .config("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider.impl.software.amazon.awssdk.auth.credentials.AwsCredentialsProvider.disabled", "true")
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9008")
        .config("spark.hadoop.fs.s3a.access.key", "admin")  
        .config("spark.hadoop.fs.s3a.secret.key", "password") 
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .config("spark.hadoop.fs.s3a.committer.name", "directory")
        .enableHiveSupport()

        .config("spark.extraListeners","datahub.spark.DatahubSparkListener") 
        .config("spark.datahub.rest.server","http://localhost:22691")

        .getOrCreate()
    )



    return spark

def write_gold_data(spark_session, folder_name, data, primary_field):

    database_name = "gold_bucket"
    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    hudi_options = {
        'hoodie.table.name': folder_name,
        'hoodie.datasource.write.recordkey.field': primary_field,
        'hoodie.datasource.write.partitionpath.field': '',
        'hoodie.datasource.write.table.name': folder_name,
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.precombine.field': primary_field,
        "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
        "hoodie.datasource.hive_sync.enable": "true",
        "hoodie.datasource.hive_sync.mode": "hms",
        "hoodie.datasource.hive_sync.jdbcurl": "thrift://localhost:9083",
        'hoodie.datasource.hive_sync.database': database_name,
        'hoodie.datasource.hive_sync.table': folder_name,
        'hoodie.datasource.hive_sync.support_timestamp': 'true',
    }

               # 'hoodie.meta.sync.datahub.emitter.server': 'http://localhost:22691',
        # 'hoodie.meta.sync.datahub.emitter.enabled': 'true',
        # 'hoodie.meta.sync.client.tool.class': 'org.apache.hudi.sync.datahub.DataHubSyncTool',
        # 'hoodie.meta.sync.datahub.hive_style_partitioning': 'true',
        # "hoodie.meta.sync.datahub.debug.enable": "true",
        # "hoodie.meta.sync.datahub.verbose": "true"

    data_path = f"s3a://warehouse/gold_bucket/{folder_name}"
    data.write.format("hudi").options(**hudi_options).mode("overwrite").save(data_path)

def summary_counts(students, staff, course, classes, program, major):
    summary = {
        "summary_id": 1,
        "total_students": students.select(countDistinct("student_code")).first()[0],
        "total_staff": staff.select(countDistinct("staff_code")).first()[0],
        "total_courses": course.select(countDistinct("course_code")).first()[0],
        "total_classes": classes.select(countDistinct("class_code")).first()[0],
        "total_programs": program.select(countDistinct("program_code")).first()[0],
        "total_majors": major.select(countDistinct("major_code")).first()[0]
    }
    return summary

SCALE = 2
def decode_decimal(binary_val):
    if binary_val is not None:
        unscaled = int.from_bytes(binary_val, byteorder='big', signed=False)
        return unscaled / (10 ** SCALE)
    return None

decode_decimal_udf = udf(decode_decimal, DoubleType())

# Student Overview 
def summary_student_stats(students):
    return students.groupBy("class_code").agg(count("*").alias("total_students"))

def student_distribution_by_program(students, classes):
    return students.join(classes, "class_code").groupBy("program_code").agg(count("*").alias("total_students"))

def graduation_by_term(graduate):
    return graduate.groupBy("term_code").agg(countDistinct("student_code").alias("graduates"))

def graduation_rate_overall(students, graduate):
    total_students = students.select(countDistinct("student_code")).first()[0]
    graduated = graduate.select(countDistinct("student_code")).first()[0]
    return spark_session.createDataFrame([Row(graduation_rate=graduated / total_students if total_students else 0)])

# Courses and Curriculum
def course_distribution_per_program(program_course):
    return program_course.groupBy("program_code").agg(countDistinct("course_code").alias("total_courses"))

def course_type_count(program_course):
    return program_course.groupBy("type").agg(count("*").alias("count"))

def course_sections_per_term(course_section):
    return course_section.groupBy("term_code").agg(count("*").alias("sections_count"))

# Academic Staff
def staff_teaching_load(course_group_detail):
    return course_group_detail.groupBy("staff_code").agg(countDistinct("course_group_code").alias("total_groups"))

def staff_by_room_usage(course_group_detail):
    return course_group_detail.groupBy("room_code").agg(countDistinct("staff_code").alias("unique_staff_count"))

# Academic Performance
def avg_score_by_term(point):
    return point.groupBy("term_code") \
                .agg(round(avg("point_4"), 2).alias("avg_gpa"))

# Classes and Programs
def total_classes_per_program(classes):
    return classes.groupBy("program_code").agg(countDistinct("class_code").alias("total_classes"))

def total_programs_per_major(program):
    return program.groupBy("major_code").agg(count("*").alias("programs_count"))

if __name__ == "__main__":
    spark_session = configure_spark_with_hudi_minio()

    classes = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/class")
    course = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/course")
    course_group = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/course_group")
    course_group_detail = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/course_group_detail")
    course_section = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/course_section")
    enrollment = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/enrollment")
    graduate = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/graduate")
    major = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/major")
    point = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/point")
    program = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/program")
    program_course = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/program_course")
    room = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/room")
    staff = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/staff")
    student = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/student")
    term = spark_session.read.format("hudi").load("s3a://warehouse/curated_bucket/school/term")

    # Dashboard: Student Overview
    data = summary_student_stats(students=student)
    write_gold_data(spark_session, "student_count_per_class", data, "class_code")

    data = student_distribution_by_program(students=student, classes=classes)
    write_gold_data(spark_session, "student_distribution_by_program", data, "program_code")

    data = graduation_by_term(graduate=graduate)
    write_gold_data(spark_session, "graduates_by_term", data, "term_code")

    data = graduation_rate_overall(students=student, graduate=graduate)
    write_gold_data(spark_session, "graduation_rate_overall", data, "graduation_rate")

    # Dashboard: Courses and Curriculum
    data = course_distribution_per_program(program_course=program_course)
    write_gold_data(spark_session, "course_distribution_per_program", data, "program_code")

    data = course_type_count(program_course=program_course)
    write_gold_data(spark_session, "course_type_count", data, "type")

    data = course_sections_per_term(course_section=course_section)
    write_gold_data(spark_session, "course_sections_per_term", data, "term_code")

    # Dashboard: Academic Staff
    data = staff_teaching_load(course_group_detail=course_group_detail)
    write_gold_data(spark_session, "staff_teaching_load", data, "staff_code")

    data = staff_by_room_usage(course_group_detail=course_group_detail)
    write_gold_data(spark_session, "staff_by_room_usage", data, "room_code")

    # Dashboard: Academic Performance
    data = avg_score_by_term(point=point)
    write_gold_data(spark_session, "avg_score_by_term", data, "term_code")

    # Dashboard: Classes and Programs
    data = total_classes_per_program(classes=classes)
    write_gold_data(spark_session, "classes_per_program", data, "program_code")

    data = total_programs_per_major(program=program)
    write_gold_data(spark_session, "programs_per_major", data, "major_code")

    spark_session.stop()

    spark_session.stop()


