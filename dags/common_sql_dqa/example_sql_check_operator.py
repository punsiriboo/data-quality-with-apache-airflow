from airflow.operators.empty import EmptyOperator
from airflow.operators.sql import SQLCheckOperator
from airflow import DAG
from datetime import datetime

# กำหนดค่า default_args สำหรับ DAG
default_args = {
    'owner': 'gemini-code-assist',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

MY_CONN_ID = 'my_retail_database'  # กำหนด MY_CONN_ID 

# สร้าง DAG
with DAG('example_sql_check_operator', 
    default_args=default_args, 
    schedule_interval='@daily',
    catchup=False,
    tags=['common-sql-provider'],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # ตรวจสอบว่ามี order ที่สร้่างหลัง 2023-01-01
    check_data_exist = SQLCheckOperator(
        task_id='check_data_exist_2023',
        sql="SELECT COUNT(*) FROM orders WHERE order_date > '2023-01-01'",
        conn_id=MY_CONN_ID,  # ใส่ชื่อ connection ใน Airflow ที่เชื่อมต่อกับฐานข้อมูล
    )

    # ตรวจสอบว่าราคาสินค้าไม่มีค่าติดลบ 
    min_price = 0
    max_price = 5000
    check_price_not_negative = SQLCheckOperator(
        task_id='check_price_not_negative',
        sql=f"""SELECT COUNT(*) FROM orders 
            WHERE price >= {min_price}
            AND price <= {max_price};""",
        conn_id=MY_CONN_ID,  # ใช้ MY_CONN_ID ที่กำหนดไว้
        retry_on_failure=True,  # retry เมื่อการตรวจสอบล้มเหลว
    )

    # ตรวจสอบว่าชื่อผู้สั่งซื้อ (customer_name) ไม่มีค่า NULL
    check_customer_name_not_null = SQLCheckOperator(
        task_id='check_customer_name_not_null',
        sql='SELECT COUNT(*) FROM orders WHERE customer_name IS​ NOT NULL;',
        conn_id=MY_CONN_ID,  # ใช้ MY_CONN_ID ที่กำหนดไว้
        retry_on_failure=True,
    )

    # ตรวจสอบความสอดคล้องของข้อมูล เช่น order_id ต้องเป็นคีย์หลัก ไม่ซ้ำกัน
    check_order_id_unique = SQLCheckOperator(
        task_id='check_order_id_unique',
        sql="""SELECT CASE WHEN COUNT(order_id) - COUNT(DISTINCT order_id) >  0 THEN 1
            ELSE 0 END AS is_unique
            FROM orders;""",
        conn_id=MY_CONN_ID,  # ใช้ MY_CONN_ID ที่กำหนดไว้
        retry_on_failure=True,
    )

    # ตรวจสอบความสอดคล้องของข้อมูลโดยเรียกจาก​ไฟล์ SQL
    check_by_sql_file = SQLCheckOperator(
        task_id='check_by_sql_file',
        sql='sql/example.sql', # เรียก query จากไฟล์ Sql
        conn_id=MY_CONN_ID,  # ใช้ MY_CONN_ID ที่กำหนดไว้
        retry_on_failure=True,
    )

    # การจัดเรียง tasks เพื่อให้รันตรวจสอบทีละขั้นตอน
    
    start >> \
    [
        check_price_not_negative, 
        check_customer_name_not_null,
        check_order_id_unique,
        check_by_sql_file
    ] >> \
    end
