from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLCheckOperator
from airflow.providers.common.sql.operators.sql_column import SQLColumnCheckOperator
from airflow.providers.common.sql.operators.sql_table import SQLTableCheckOperator
from airflow.utils.dates import days_ago

# กำหนดค่าเริ่มต้นสำหรับ DAG
default_args = {
    'owner': 'airflow',
}

# สร้าง DAG ชื่อ `sql_data_quality_check`
with DAG(
    dag_id='sql_data_quality_check',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # ตัวอย่าง SQLCheckOperator - ตรวจสอบเงื่อนไขทั่วไปในตาราง
    check_data_exist = SQLCheckOperator(
        task_id='check_data_exist',
        sql="SELECT COUNT(*) FROM orders WHERE order_date > '2023-01-01'",
        conn_id='my_sql_connection',  # ใส่ชื่อ connection ใน Airflow ที่เชื่อมต่อกับฐานข้อมูล
    )

    # ตัวอย่าง SQLColumnCheckOperator - ตรวจสอบคอลัมน์ในตาราง
    column_checks = SQLColumnCheckOperator(
        task_id='column_checks',
        table='orders',
        column_mapping={
            'price': {'min': 0},  # ตรวจสอบว่าราคาไม่มีค่าติดลบ
            'quantity': {'max': 100},  # ตรวจสอบว่า quantity ไม่เกิน 100
        },
        conn_id='my_sql_connection',
    )

    # ตัวอย่าง SQLTableCheckOperator - ตรวจสอบระดับตาราง
    table_checks = SQLTableCheckOperator(
        task_id='table_checks',
        table='orders',
        checks={
            'row_count_check': {'check_statement': 'COUNT(*) > 1000'},  # ตรวจสอบว่ามีจำนวนแถวมากกว่า 1,000 แถว
            'unique_order_id_check': {'check_statement': 'COUNT(DISTINCT order_id) = COUNT(order_id)'},  # ตรวจสอบว่า `order_id` ไม่ซ้ำกัน
        },
        conn_id='my_sql_connection',
    )

    # กำหนดลำดับการทำงาน
    check_data_exist >> column_checks >> table_checks
