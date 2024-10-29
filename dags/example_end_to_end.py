from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.google.cloud.transfers.bigquery import BigQueryColumnCheckOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
import pandas as pd
from include.commons.slack_client import send_success_notify, send_failed_notiy

# Replace with your project ID and BigQuery details
MY_CONN_ID = "my_retail_database"
PROJECT_ID = 'your-project-id'
DATASET_ID = 'your_dataset_id'
TABLE_ID = 'orders'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_success_callback': send_success_notify,
    'on_failure_callback': send_failed_notiy
}

with DAG(
    'order_to_bigquery',
    default_args=default_args,
    description='Extract, transform, and load data from SQLite to BigQuery',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # Task 1: Extract data from SQLite
    extract_data = SqliteOperator(
        task_id='extract_data',
        sqlite_conn_id='sqlite_default',  # Make sure to configure this connection in Airflow
        sql='SELECT * FROM orders where order_date = {execution_date};',
        do_xcom_push=True,
    )

    # Task 2: Transform data using Pandas
    def transform_data(**kwargs):
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='extract_data')
        df = pd.DataFrame(data, columns=['order_id', 'order_date', 'channel', 'customer_name', 'product_name', 'price', 'quantity', 'status'])
        df['order_date'] = pd.to_datetime(df['order_date'])
        ti.xcom_push(key='transformed_data', value=df.to_json(orient='records'))
        ti.xcom_push(key='cnt_order_transform', value=len(df))

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )
    
    def reconciliation_checks(**kwargs):
        ti = kwargs['ti']
        cnt_order_transform = ti.xcom_pull(key='cnt_order_transform')
        print(cnt_order_transform)
        assert cnt_order_transform == 100 , "Check number of rows count"

    # Task 3: Load data into a temporary BigQuery table
    load_to_temp_table = BigQueryInsertJobOperator(
        task_id='load_to_temp_table',
        configuration={
            'jobType': 'QUERY',
            'query': {
                'query': f"""
                    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.temp_orders` AS 
                    SELECT * FROM UNNEST(@transformed_data)
                """,
                'useLegacySql': False,
                'parameterMode': 'NAMED',
                'queryParameters': [
                    {
                        'name': 'transformed_data',
                        'parameterType': {'type': 'ARRAY', 'arrayType': {'type': 'STRUCT'}},
                        'parameterValue': {'arrayValues': [{'structValues': {}}]}
                    }
                ]
            }
        }
    )

    # Task 4: Merge data from the temporary table to the main table
    INSERT_DATA_QUERY = f"""
        INSERT INTO `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` (order_id, order_date, channel, customer_name, product_name, price, quantity, status)
        SELECT order_id, order_date, channel, customer_name, product_name, price, quantity, status
        FROM `{PROJECT_ID}.{DATASET_ID}.temp_orders`;
    """
    merge_data = BigQueryInsertJobOperator(
        task_id='merge_data',
        configuration={
            'jobType': 'QUERY',
            'query': {'query': INSERT_DATA_QUERY, 'useLegacySql': False}
        }
    )

    column_checks = BigQueryColumnCheckOperator(
        task_id='column_checks',
        table='orders',
        column_mapping={
            'order_id': {
                "unique_check": {"equal_to": 0},
                "null_check": {"equal_to": 0}
            },
            'price': {
                "null_check": {"equal_to": 0},
                "min": {"greater_than": 0}
            },  
            'quantity': {
                "min": {"greater_than": 0}, 
                "max": {"leq_to": 1000}
            },
        },
        conn_id=MY_CONN_ID,
    )

    # Task dependencies
    start >> \
    extract_data >> \
    transform_data >> \
    load_to_temp_table >> \
    [
        column_checks >> \
        reconciliation_checks
    ] >> \
    merge_data >> \
    end
