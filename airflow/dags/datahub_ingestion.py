from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import pytz


local_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

with DAG(
    dag_id='ingest_curated_bucket',
    start_date=datetime(2024, 10, 10, tzinfo=local_timezone),
    schedule='25 * * * *',
    catchup=False
    ) as dag:
        trino_ingest = BashOperator(
            task_id = 'ingest_curated_bucket',
            bash_command='source /dis/datahub/trinovenv/bin/activate && datahub ingest -c /dis/datahub/trino-ingest.yml',
            cwd='/dis'
        )

        trino_ingest
        