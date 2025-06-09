from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import pytz

from datahub_airflow_plugin.entities import Dataset, Urn

local_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

with DAG(
    dag_id='aggregate_bucket',
    start_date=datetime(2024, 10, 10, tzinfo=local_timezone),
    schedule='0 0 1 * *',
    catchup=False
    ) as dag:
        process_raw_data = BashOperator(
            task_id='process_raw_data',
            bash_command='source /dis/test_spark/venv/bin/activate && python /dis/data_storage/consumer/tables/curated_bucket/write_to_curated_bucket.py',
            cwd='/dis'
        )

        generate_gold_data = BashOperator(
            task_id = 'generate_gold_data',
            bash_command='source /dis/test_spark/venv/bin/activate && python /dis/data_storage/consumer/tables/gold_bucket/write_to_gold_bucket.py',
            cwd='/dis'
        )

        process_raw_data >> generate_gold_data