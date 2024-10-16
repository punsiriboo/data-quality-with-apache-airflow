# [DataTH] Data Quality with Apache Airflow

<p align="center" width="100%">
    <img src="./assets/course_title.png"> 
</p>

## 🎉 แนะนำตัว
ผู้สอน: ปุณณ์สิริ บุณยเกียรติ (บีท) </br>
Senior Data Engineer, CJ MORE

## 🗓️ สิ่งที่คุณจะได้พบ

ใน Workshop วันนี้เราจะครอบคลุมหัวข้อต่าง ๆ ดังนี้:

### Data Quality Assurance in Apache Airflow
1. [Setup Google Cloud Environment](documents/01_set_up_gemini_code_assist.md)
2. [Set up local Airflow environment](documents/02_set_up_airflow_env.md)

### Folder Explaination 
```md
data-quality-with-apache-airflow/
│
├── README.md
└── assets/
└── dags/
└── runable_dags/
└── documents/
└── prompts/
└── cred/
└── tests/
└── include/
```

| Name | Description |
| - | - |
| `assets/` | โฟลเดอร์ที่เก็บ assets เช่นรูปภาพต่างๆ หรือ diagram
| `dags/` | โฟลเดอร์ที่เก็บโค้ด DAG หรือ Airflow Data Pipelines ที่เราสร้างจะใช้ใน workshop |
| `runable_dags/` | โฟลเดอร์ที่เก็บโค้ด DAG หรือ Airflow Data Pipelines ที่เป็นเฉลยของ workshop ใช้งานได้  |
| `docker-compose.yaml` | ไฟล์ Docker Compose ที่ใช้รัน Airflow ขึ้นมาบนเครื่อง |
| `prompts/`| โฟลเดอร์ที่เก็บ prompts ที่ใช้ในการ Generate Code หรือ Query
| `cred/` | โฟลเดอร์ที่เก็บไฟล์ Credential หรือ Configuration อย่างไฟล์ `sa.json` |
| `tests/` | โฟลเดอร์ที่เก็บไฟล์ unitest เพื่อทำการทดสอบ python code |
| `include/` | โฟลเดอร์ที่เก็บ commons หรือ external integrate กับ open-source อื่นเช่น greate expactation |
