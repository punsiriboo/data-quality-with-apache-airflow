# [Skooldio DEB] Gemini Code Assist for Data Engineering


## 2.Preparing the Airflow DAG Development Environment
ใน Bootcamp โปรเจคนี้ เราจะสร้าง Data Pipeline ในโฟลเดอร์ 00-bootcamp-project ดังนั้นให้เราคัดลอกไฟล์ docker-compose-with-spark.yml จากโฟลเดอร์ 04-automated-data-pipelines มาสร้างเป็นไฟล์ชื่อ docker-compose.yml มาใช้งาน


```sh
mkdir -p ./dags ./config ./logs ./plugins ./tests
```
​
สำหรับเครื่องที่เป็น Linux เราจำเป็นที่จะต้องกำหนด Airflow user ก่อนด้วย เพื่อให้ Airflow user ที่อยู่ใน Docker container สามารถเขียนไฟล์ลงมาบนเครื่อง host ได้ เราจะใช้คำสั่ง

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```sh
docker-compose up
```
