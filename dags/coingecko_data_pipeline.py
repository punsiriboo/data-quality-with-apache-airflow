import sys
import requests
import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook


COMMONS_PATH ="/opt/airflow/include/"
if not COMMONS_PATH in sys.path:
    sys.path.insert(0, COMMONS_PATH)

from commons.slack_client import send_success_notify

# Define default arguments for the DAG
default_args = {
    'owner': 'gemini-code-assist',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'sla': timedelta(minutes=1) # Set SLA to 1 minutes
}

__doc__ = """
This DAG collects cryptocurrency price data from the CoinGecko API and loads it into a BigQuery table.

**Schedule:**

The DAG runs every Monday, Wednesday, and Friday at midnight.

**Tasks:**

1. **collect_coingecko_data:**
    - Fetches price data for Bitcoin, Ethereum, and Tether in USD and THB.
    - Includes market cap, 24-hour volume, 24-hour change, and last updated timestamp.
    - Converts the timestamp to a datetime object.
    - Uploads the data as a JSON file to Google Cloud Storage (GCS).

2. **load_to_bigquery:**
    - Loads the JSON data from GCS into a BigQuery table.
    - Appends new data to the existing table.
    - Creates the table if it doesn't exist.

**Dependencies:**

- `collect_coingecko_data` runs before `load_to_bigquery`.

**Configuration:**

- Replace `deb-gemini-code-assist-beat-99` with your actual GCS bucket name.
- Ensure that the BigQuery table `gemini_assist_workshop.coingecko_price` exists or is created.

**Notes:**

- The CoinGecko API has rate limits. Ensure you don't exceed these limits.
- The `schedule_interval` can be adjusted to suit your needs.
- The `write_disposition` can be changed to `WRITE_TRUNCATE` if you want to overwrite the table with new data.
"""

with DAG(
    'coingecko_api_to_bigquery',
    default_args=default_args,
    description='Collect data from CoinGecko API and load to BigQuery',
    schedule_interval='*/3 * * * *',  # Run every 3 minutes
    start_date=datetime(2024, 10, 10),
    catchup=False,
    doc_md = __doc__,
    on_success_callback=send_success_notify,
    sla_miss_callback=None,
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # Task 1: Collect data from CoinGecko API
    def collect_coingecko_data(**kwargs):
        api_url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin,ethereum,tether',
            'vs_currencies': 'usd,thb',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true',
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        # Convert timestamp to datetime object
        for coin, values in data.items():
            data[coin]['last_updated_at'] = datetime.fromtimestamp(values['last_updated_at']).isoformat()

        # Upload JSON data to GCS
        bucket_name = kwargs['bucket_name']
        gcs_folder = 'raw/coingecko'
        gcs_hook = GCSHook()
        gcs_hook.upload(
            bucket_name=bucket_name,
            object_name=f'{gcs_folder}/coingecko_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            data=json.dumps(data),
        )

    collect_data_task = PythonOperator(
        task_id='collect_coingecko_data',
        python_callable=collect_coingecko_data,
        op_kwargs={'bucket_name': 'deb-gemini-code-assist-beat-99'},  # Replace with your bucket name
        sla=timedelta(seconds=10) # Set SLA to 10 seconds
    )

    # Task 2: Load data from GCS to BigQuery
    load_to_bq_task = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket='deb-gemini-code-assist-beat-99',  # Replace with your bucket name
        source_objects=['raw/coingecko/*.json'],  # Load all JSON files in the folder
        destination_project_dataset_table='gemini_assist_workshop.coingecko_price',
        write_disposition='WRITE_APPEND',  # Append data to the table
        source_format='NEWLINE_DELIMITED_JSON',
        create_disposition='CREATE_IF_NEEDED',  # Create the table if it doesn't exist
    )

    # Set task dependencies
    start >> \
    collect_data_task >> \
    load_to_bq_task >> \
    end
