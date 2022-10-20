from datetime import timedelta
import airflow
import pandas as pd
import numpy as np
import os 


from airflow import DAG
from airflow.operators.python import PythonOperator

def read_data():
    titanic = pd.read_csv("data/titanic_test.csv")
    titanic.to_csv('data/titanic.txt', sep='\t')

def show_message():
    print("pandas df convrted to txt")

default_args = {
 'owner':'airflow',
 'depends_on_past' : False,
 'start_date': airflow.utils.dates.days_ago(7)
}

df_transform_dag = DAG(
    'df_transform_dag', #name of the dag
    default_args = default_args,
    schedule_interval = timedelta(days=30),
    catchup = False

)

reading_data = PythonOperator(
    task_id='reading_data',
    python_callable = read_data,
    dag = df_transform_dag,
)

showing_message = PythonOperator(
    task_id = 'transformed_data_message',
    python_callable = show_message,
    dag = df_transform_dag,
)
reading_data >> showing_message