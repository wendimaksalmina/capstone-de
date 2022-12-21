from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

from coindesk_script import store_coindesk_to_bq

with DAG(
    dag_id="coindesk_scheduler",
    start_date=pendulum.datetime(year=2022, month=12, day=21, tz='Asia/Jakarta'),
    schedule_interval="* 9 * * *"
    ) as dag:
        
        store_coindesk = PythonOperator(
            task_id="store_coindesk",
            python_callable=store_coindesk_to_bq
        )

        store_coindesk