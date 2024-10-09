from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG using the 'with' statement
with DAG(
    'example_xcom_dag',
    default_args=default_args,
    description='Example DAG with XCom',
    schedule_interval=None,  # Run manually
) as dag:

    def task_1(**kwargs):
        my_name = "John Doe"
        print(f"My name is: {my_name}")
        kwargs['ti'].xcom_push(key='name', value=my_name)

    def task_2(**kwargs):
        pulled_name = kwargs['ti'].xcom_pull(key='name', task_ids='task_1')
        print(f"Hello, {pulled_name}!")

    t1 = PythonOperator(
        task_id='task_1',
        python_callable=task_1,
    )

    t2 = PythonOperator(
        task_id='task_2',
        python_callable=task_2,
    )

    t1 >> t2
