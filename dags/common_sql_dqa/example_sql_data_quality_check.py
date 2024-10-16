import sys
import airflow
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import (
    SQLCheckOperator, 
    SQLColumnCheckOperator, 
    SQLValueCheckOperator,
    SQLTableCheckOperator,
    SQLThresholdCheckOperator,
    SQLIntervalCheckOperator
) 
from airflow.utils.dates import days_ago

COMMONS_PATH ="/opt/airflow/include/"
if not COMMONS_PATH in sys.path:
    sys.path.insert(0, COMMONS_PATH)

from commons.slack_client import send_success_notify, send_failed_notiy

# กำหนดค่าเริ่มต้นสำหรับ DAG
default_args = {
    'owner': 'punsiri.boo',
    "start_date": airflow.utils.dates.days_ago(1)
}

MY_CONN_ID = 'my_retail_database'

# สร้าง DAG ชื่อ `example_sql_data_quality_check`
with DAG(
    dag_id='example_sql_data_quality_check',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
    tags=['common-sql-provider'],
    on_failure_callback=send_failed_notiy,
    on_success_callback=send_success_notify
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # ตัวอย่าง SQLCheckOperator - ตรวจสอบเงื่อนไขทั่วไปในตาราง
    check_data_exist = SQLCheckOperator(
        task_id='check_data_exist',
        sql="SELECT COUNT(*) FROM orders WHERE order_date > '2023-01-01'",
        conn_id=MY_CONN_ID,  # ใส่ชื่อ connection ใน Airflow ที่เชื่อมต่อกับฐานข้อมูล
    )

    # ตัวอย่าง SQLColumnCheckOperator - ตรวจสอบคอลัมน์ในตาราง
    """
    SQLColumnCheckOperator ใช้เพื่อตรวจสอบความถูกต้องของคอลัมน์ในตาราง 'orders' 
    โดยมีเงื่อนไขการตรวจสอบตามที่ระบุใน column_mapping

    - 'order_id':
        - "unique_check": ตรวจสอบว่าค่าซ้ำมีจำนวนเท่ากับ 0
        - "null_check": ตรวจสอบว่าค่า null มีจำนวนเท่ากับ 0

    - 'price':
        - "null_check": ตรวจสอบว่าคอลัมน์ price ไม่มีค่า null
        - "min": ตรวจสอบว่าราคาจะไม่มีค่าติดลบ 

    - 'quantity':
        - "min": ตรวจสอบว่าค่าของ quantity มากกว่า 0
        - "max": ตรวจสอบว่าค่าของ quantity น้อยกว่าหรือเท่ากับ 1000 
    """
    column_checks = SQLColumnCheckOperator(
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

    # ตัวอย่าง SQLTableCheckOperator - ตรวจสอบระดับตาราง
    """
    SQLTableCheckOperator ใช้สำหรับตรวจสอบความถูกต้องของข้อมูลระดับตาราง

    - table: 'orders' คือ ตารางที่เราจะทำการตรวจสอบ
    - checks: กำหนดเงื่อนไขการตรวจสอบในระดับตาราง เช่น
        - 'row_count_check': ตรวจสอบว่าจำนวนแถวในตารางต้องมากกว่า 10 (`COUNT(*) > 10`)
        - 'unique_order_id_check': ตรวจสอบว่า `order_id` ต้องไม่ซ้ำกัน โดยตรวจสอบว่า 
          จำนวนค่า `DISTINCT` ของ `order_id` เท่ากับจำนวน `order_id` ทั้งหมด

    - conn_id: 'my_retail_database' คือ Connection ID ของฐานข้อมูลที่ใช้ในการเชื่อมต่อ
    """
    table_checks = SQLTableCheckOperator(
        task_id='table_checks',
        table='orders',
        checks={
            'row_count_check': {'check_statement': 'COUNT(*) > 10'},  # ตรวจสอบว่ามีจำนวนแถวมากกว่า 1,000 แถว
            'unique_order_id_check': {'check_statement': 'COUNT(DISTINCT order_id) = COUNT(order_id)'},  # ตรวจสอบว่า `order_id` ไม่ซ้ำกัน
        },
        partition_clause="status = 'Complete'",
        conn_id=MY_CONN_ID,
    )

    value_check = SQLValueCheckOperator(
        task_id="check_row_count",
        sql=f"SELECT COUNT(*) FROM orders;",
        pass_value=200, #คาดหวังว่าจะมี จำนวน record ต้องเท่ากับ 200
        conn_id=MY_CONN_ID,
    )

    # ตัวอย่าง SQLValueCheckOperator - ตรวจสอบ value ระดับ column ระบุขอบเขตของค่า
    threshold_check = SQLThresholdCheckOperator(
        task_id="check_threshold",
        sql=f"SELECT AVG(quantity) FROM orders;",
        min_threshold=1,# ค่าเฉลี่ยนของจำนวนชิ้นของการสั้งซื้อไม่ควรต่ำกว่า 1 ชิ้น
        max_threshold=5, # ค่าเฉลี่ยนของจำนวนชิ้นของการสั้งซื้อไม่ควรเกิน 5 ชิ้น
        conn_id=MY_CONN_ID, #'my_retail_database' คือ Connection ID ของฐานข้อมูลที่ใช้ในการเชื่อมต่อ
    )

    # ตัวอย่าง SQLIntervalCheckOperator - ค่าเทียบกับช่วงเวลาก่อนหน้า
    interval_check = SQLIntervalCheckOperator(
        task_id="check_interval_data",
        table="orders",
        days_back=-1,
        date_filter_column="order_date",
        metrics_thresholds={"AVG(quantity)": 1.5},
        conn_id=MY_CONN_ID, #'my_retail_database' คือ Connection ID ของฐานข้อมูลที่ใช้ในการเชื่อมต่อ
    )

    # กำหนดลำดับการทำงาน
    start >> \
        [
            check_data_exist,
            column_checks,
            table_checks,
            value_check,
            threshold_check,
            interval_check,
        ] >> \
    end

