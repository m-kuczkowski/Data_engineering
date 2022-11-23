from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from etl_function import run_api_etl
 

default_args = { 
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime('2022', '11', '24'),
    'email': 'airflow@example.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)}

dag = DAG(
    'covid_dag',
    default_args=default_args,
    description = 'elt code for covid api'
)

run_etl = PythonOperator(
    task_id = 'complete_covid_etl',
    python_callable=run_api_etl,
    dag=dag
)

run_etl
