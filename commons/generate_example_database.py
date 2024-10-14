import sqlite3
from faker import Faker
import random

SQL_LITE_DB = '/data/example_retail.db'

# Create a Faker instance
fake = Faker()

def create_order_table():
    # สร้างการเชื่อมต่อไปยังฐานข้อมูล (ถ้ายังไม่มีไฟล์ฐานข้อมูล ระบบจะสร้างให้)
    conn = sqlite3.connect(SQL_LITE_DB)

    # สร้าง Cursor สำหรับใช้ในการรันคำสั่ง SQL
    cursor = conn.cursor()

    # สร้างตารางใหม่ชื่อว่า `orders`
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,  -- กำหนดให้ order_id เป็น Primary Key
            order_date DATE NOT NULL,      -- คอลัมน์วันที่สั่งซื้อ ไม่อนุญาตให้มีค่า NULL
            customer_name TEXT NOT NULL,   -- คอลัมน์ชื่อผู้สั่งซื้อ
            product_name TEXT NOT NULL,    -- ชื่อสินค้า
            price REAL,  -- ราคาสินค้า ห้ามมีค่าติดลบ (>= 0)
            quantity INTEGER  -- จำนวนสินค้าที่สั่งซื้อ ต้องไม่เกิน 100
        );
    ''')

    # เพิ่มข้อมูลลงในตาราง
    # Generate sample data using Faker
    sample_data = []
    for _ in range(100):  # Generate 10 records
        order_id = fake.unique.random_int(min=1, max=1000)
        order_date = fake.date_between(start_date='2023-01-01', end_date='2023-04-30')
        customer_name = fake.first_name()
        product_name = random.choice(['Laptop', 'Headphones', 'Smartphone', 'Monitor', 'Keyboard', 'Mouse', 'Tablet', 'Smartwatch', 'Camera'])
        price = round(random.uniform(10.0, 1000.0), 2)
        quantity = random.randint(1, 5)

        sample_data.append((order_id, order_date, customer_name, product_name, price, quantity))

    # SQL statement to insert data
    cursor.executemany("""
        INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, sample_data)

    cursor.execute("""
    -- เพิ่มตัวอย่างข้อมูลซ้ำกัน (เพื่อใช้ทดสอบ unique_order_id_check)
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (101, '2023-02-15', 'Bob', 'Headphones', 30.0, 2);
    """)
                
    cursor.execute("""
    -- เพิ่มข้อมูลที่ไม่ตรงกับเงื่อนไขสำหรับทดสอบ column_checks (price ติดลบ)
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (102, '2023-02-15', 'Test User', 'Test Product', -5.0, 1);
    """)

    cursor.execute("""
    -- เพิ่มข้อมูลที่ไม่ตรงกับเงื่อนไขสำหรับทดสอบ quantity (quantity มากกว่า 100)
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (103, '2023-03-01', 'Test User 2', 'Test Product 2', 10.0, 150);           
    """)

    # บันทึกการเปลี่ยนแปลง
    conn.commit()

    # ดึงข้อมูล นับจำนวน `orders`
    cursor.execute("SELECT count(*) FROM orders")
    rows = cursor.fetchall()

    # แสดงผลข้อมูลที่ได้
    print("orders count:")
    for row in rows:
        print(row)

    # ปิดการเชื่อมต่อ
    conn.close()

if __name__ == "__main__":
    create_order_table()