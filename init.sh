#!/bin/bash

# Create directories
mkdir -p ./{config,dags,db,logs,plugins}

# Create .env file with AIRFLOW_UID
echo -e "AIRFLOW_UID=$(id -u)" > .env

echo "Initialization complete."