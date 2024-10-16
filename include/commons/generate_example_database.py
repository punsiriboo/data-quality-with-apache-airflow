import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta


SQL_LITE_DB = 'data/example_retail.db'

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
            channel TEXT NOT NULL,    -- ช่องทองการซื้อสินค้า ไม่อนุญาตให้มีค่า NULL
            customer_name TEXT NOT NULL,   -- คอลัมน์ชื่อผู้สั่งซื้อ
            product_name TEXT NOT NULL,    -- ชื่อสินค้า
            price REAL,  -- ราคาสินค้า ห้ามมีค่าติดลบ (>= 0)
            quantity INTEGER, -- จำนวนสินค้าที่สั่งซื้อ ต้องไม่เกิน 100
            status TEXT NOT NULL -- สถานะการสั่งซื้อ
        );
    ''')

    # เพิ่มข้อมูลลงในตาราง
    # Generate sample data using Faker
    channel_choice = ["Website", "Mobile App", "In-store"]
    product_choice = ['Laptop', 'Headphones', 'Smartphone', 'Monitor', 'Keyboard', 'Mouse', 'Tablet', 'Smartwatch', 'Camera']
    status_choice = ["Cancelled", "Complete", "Processing", "Returned", "Shipped"]
    insert_stmt = "INSERT INTO orders (order_id, order_date, channel, customer_name, product_name, price, quantity, status)"
    for i in range(100):  # Generate 10 records
        order_id = i + 1
        order_date = fake.date_this_month().strftime('%Y-%m-%d')
        channel = random.choice(channel_choice)
        customer_name = fake.first_name()
        product_name = random.choice(product_choice)
        price = round(random.uniform(10.0, 1000.0), 2)
        quantity = random.randint(1, 5)
        status = random.choice(status_choice)

        sample_data = (order_id, order_date, channel, customer_name, product_name, price, quantity, status)
        print(sample_data)

        stmt = f"""
            {insert_stmt}
            VALUES {sample_data};
        """

        print(stmt)
        cursor.execute(stmt)

    # Get today's date
    today = datetime.today()

    # Get yesterday's date
    yesterday = today - timedelta(days=1)

    cursor.execute(f"""
    -- เพิ่มตัวอย่างข้อมูลซ้ำกัน (เพื่อใช้ทดสอบ unique_order_id_check)
    {insert_stmt} VALUES
    (101, '{yesterday.strftime('%Y-%m-%d')}', 'Website', 'Bob', 'Headphones', 30.0, 2, 'Complete');
    """)
                
    cursor.execute(f"""
    -- เพิ่มข้อมูลที่ไม่ตรงกับเงื่อนไขสำหรับทดสอบ column_checks (price ติดลบ)
    {insert_stmt} VALUES
    (102,  '{today.strftime('%Y-%m-%d')}', 'Website', 'Test User', 'Test Product', -5.0, 1, 'Cancelled');
    """)

    cursor.execute(f"""
    -- เพิ่มข้อมูลที่ไม่ตรงกับเงื่อนไขสำหรับทดสอบ quantity (quantity มากกว่า 100)
    {insert_stmt} VALUES
    (103,  '{today.strftime('%Y-%m-%d')}', 'Website', 'Test User 2', 'Test Product 2', 10.0, 150, 'Complete');         
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