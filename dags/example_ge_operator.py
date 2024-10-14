from airflow import DAG
from airflow.operators.empty import EmptyOperator
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)
from airflow.utils.dates import days_ago

MY_CONN_ID = "my_retail_database"
MY_DB_SCHEMA = "orders"
MY_GX_DATA_CONTEXT = "include/gx"

# Define the DAG

default_args = {
    'owner': 'punsiri.boo',
}

with DAG(
    dag_id="example_ge_operator",
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    default_args=default_args
) as dag:
    
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # Task: Validate the data using Great Expectations
    validate_orders_table_level = GreatExpectationsOperator(
        task_id="validate_orders_table_level",
        conn_id=MY_CONN_ID,
        data_context_root_dir=MY_GX_DATA_CONTEXT,
        data_asset_name="orders",  # Your data asset name
        expectation_suite_name="orders_table_validation_suite",  # Your expectation suite name
        return_json_dict=True,  # Returns validation results as a dictionary
    )

    validate_orders_columns_level = GreatExpectationsOperator(
        task_id="validate_orders_columns_level",
        conn_id=MY_CONN_ID,
        data_context_root_dir=MY_GX_DATA_CONTEXT,
        data_asset_name="orders",  # Your data asset name
        expectation_suite_name="orders_columns_validation_suite",  # Your expectation suite name
        return_json_dict=True,  # Returns validation results as a dictionary
    )

    # กำหนดลำดับการทำงาน
    start >> \
    validate_orders_table_level >> \
    validate_orders_columns_level >> \
    end
        