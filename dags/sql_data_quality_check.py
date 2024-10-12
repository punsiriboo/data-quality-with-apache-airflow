from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLCheckOperator
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator, SQLTableCheckOperator
from airflow.utils.dates import days_ago

# กำหนดค่าเริ่มต้นสำหรับ DAG
default_args = {
    'owner': 'punsiri.boo',
}

# สร้าง DAG ชื่อ `sql_data_quality_check`
with DAG(
    dag_id='sql_data_quality_check',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # ตัวอย่าง SQLCheckOperator - ตรวจสอบเงื่อนไขทั่วไปในตาราง
    check_data_exist = SQLCheckOperator(
        task_id='check_data_exist',
        sql="SELECT COUNT(*) FROM orders WHERE order_date > '2023-01-01'",
        conn_id='my_retail_database',  # ใส่ชื่อ connection ใน Airflow ที่เชื่อมต่อกับฐานข้อมูล
    )

    # ตัวอย่าง SQLColumnCheckOperator - ตรวจสอบคอลัมน์ในตาราง
    """
    ใช้ SQLColumnCheckOperator เพื่อตรวจสอบความถูกต้องของคอลัมน์ในตาราง 'orders' 
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
                # TODO: แก้เพื่อตรวจสอบว่าราคาไม่มีค่าติดลบ
                "min": {"greater_than": -10}
            },  
            'quantity': {
                "min": {"greater_than": 0}, 
                "max": {"leq_to": 1000}
            },
        },
        conn_id='my_retail_database',
    )

    # ตัวอย่าง SQLTableCheckOperator - ตรวจสอบระดับตาราง
    table_checks = SQLTableCheckOperator(
        task_id='table_checks',
        table='orders',
        checks={
            'row_count_check': {'check_statement': 'COUNT(*) > 10'},  # ตรวจสอบว่ามีจำนวนแถวมากกว่า 1,000 แถว
            'unique_order_id_check': {'check_statement': 'COUNT(DISTINCT order_id) = COUNT(order_id)'},  # ตรวจสอบว่า `order_id` ไม่ซ้ำกัน
        },
        conn_id='my_retail_database',
    )

    # กำหนดลำดับการทำงาน
    start >> check_data_exist >> column_checks >> table_checks >> end

