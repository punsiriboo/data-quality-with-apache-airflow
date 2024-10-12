import sqlite3

def create_database():
    # 1. สร้างการเชื่อมต่อไปยังฐานข้อมูล (ถ้ายังไม่มีไฟล์ฐานข้อมูล ระบบจะสร้างให้)
    conn = sqlite3.connect('/opt/airflow/data/example_retail.db')

    # 2. สร้าง Cursor สำหรับใช้ในการรันคำสั่ง SQL
    cursor = conn.cursor()

    # 3. สร้างตารางใหม่ชื่อว่า `orders`
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

    # 4. เพิ่มข้อมูลลงในตาราง
    cursor.execute("""
    -- เพิ่มข้อมูลตัวอย่างลงในตาราง orders
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (1, '2023-02-10', 'Alice', 'Laptop', 900.0, 1),
    (2, '2023-02-15', 'Bob', 'Headphones', 30.0, 2),
    (3, '2023-03-01', 'Charlie', 'Smartphone', 600.0, 1),
    (4, '2023-03-05', 'David', 'Monitor', 150.0, 2),
    (5, '2023-01-05', 'Eve', 'Keyboard', 20.0, 5),
    (6, '2023-01-20', 'Alice', 'Mouse', 15.0, 3),
    (7, '2023-02-20', 'Bob', 'Tablet', 300.0, 1),
    (8, '2023-03-10', 'Charlie', 'Laptop', 950.0, 1),
    (9, '2023-04-01', 'David', 'Smartwatch', 120.0, 1),
    (10, '2023-04-05', 'Eve', 'Camera', 500.0, 2);

    """)

    cursor.execute("""
    -- เพิ่มตัวอย่างข้อมูลซ้ำกัน (เพื่อใช้ทดสอบ unique_order_id_check)
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (11, '2023-02-15', 'Bob', 'Headphones', 30.0, 2);
    """)
                
    cursor.execute("""
    -- เพิ่มข้อมูลที่ไม่ตรงกับเงื่อนไขสำหรับทดสอบ column_checks (price ติดลบ)
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (12, '2023-02-15', 'Test User', 'Test Product', -5.0, 1);
    """)

    cursor.execute("""
    -- เพิ่มข้อมูลที่ไม่ตรงกับเงื่อนไขสำหรับทดสอบ quantity (quantity มากกว่า 100)
    INSERT INTO orders (order_id, order_date, customer_name, product_name, price, quantity) VALUES
    (13, '2023-03-01', 'Test User 2', 'Test Product 2', 10.0, 150);
                
    """)

    # 5. บันทึกการเปลี่ยนแปลง
    conn.commit()

    # 6. ดึงข้อมูล นับจำนวน `orders`
    cursor.execute("SELECT count(*) FROM orders")
    rows = cursor.fetchall()

    # 7. แสดงผลข้อมูลที่ได้
    print("orders count:")
    for row in rows:
        print(row)

    # 8. ปิดการเชื่อมต่อ
    conn.close()

if __name__ == "__main__":
    create_database()