# ตัวอย่างการปรับ stock_ingestion_dag.py ให้เรียกใช้ extract_stock.py
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 4, 25),
    'retries': 1,
}

with DAG(
    'stock_ingestion_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:

    # ใช้ BashOperator สั่งรันไฟล์ Script ที่คุณเขียนไว้
    run_extract = BashOperator(
        task_id='run_extract_script',
        bash_command='python /opt/airflow/scripts/extract_stock.py' 
    )