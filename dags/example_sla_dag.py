import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from time import sleep

COMMONS_PATH ="/opt/airflow/include/"
if not COMMONS_PATH in sys.path:
    sys.path.insert(0, COMMONS_PATH)

from commons.slack_client import send_fail_notiy


default_args = {
    'owner': 'punsiri.boo',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'example_sla_dag',
    default_args=default_args,
    description='Example DAG with SLA',
    schedule_interval='*/3 * * * *',  # Run every 3 minutes
    start_date=datetime(2023, 12, 20),
    catchup=False,
    sla_miss_callback=send_fail_notiy,
) as dag:

    def my_task(**kwargs):
        sleep(10)  # Simulate a task that takes 10 seconds
        print("Task completed!")

    task = PythonOperator(
        task_id='my_task',
        python_callable=my_task,
        sla=timedelta(seconds=5),  # Set SLA to 5 seconds
    )

    task
    
# Run this dag with `airflow tasks test example_sla_dag my_task`