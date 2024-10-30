# Gemini Code Assist for Data Engineering


## 2.Preparing the Airflow DAG Development Environment
ทำการรันเพื่อสร้าง docker

```sh
mkdir -p ./dags ./config ./logs ./plugins ./tests ./cred
```
​
สำหรับเครื่องที่เป็น Linux เราจำเป็นที่จะต้องกำหนด Airflow user ก่อนด้วย เพื่อให้ Airflow user ที่อยู่ใน Docker container สามารถเขียนไฟล์ลงมาบนเครื่อง host ได้ เราจะใช้คำสั่ง

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```sh
docker compose up
```

#### Docker Commands
- Build custom Airflow Image: `docker compose build`
- Spin Up Docker Containers: `docker compose up -d`
- Stop Docker Containers: docker `compose stop`
- Start stopped Docker Containers: `docker compose start`
- Destroy Docker Containers: `docker compose down --volumes --remove-orphans`