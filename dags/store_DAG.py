from xml.dom.pulldom import default_bufsize
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator
from datacleaner import data_cleaner 

# define yesterday's date 
yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')


default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2022, 7, 2),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

dag=DAG('store_dag', default_args=default_args, schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'] ,catchup=False)


# to check if file exists 
t1=BashOperator(task_id='check_file_exists', bash_command='shasum ~/store_files_airflow/raw_store_transactions.csv',  retries=2, retry_delay=timedelta(seconds=15), dag=dag)


# Clean the Data 
t2 = PythonOperator(task_id='clean_raw_csv', python_callable=data_cleaner, dag=dag)


# Create a mysql table 

t3 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_table.sql", dag=dag)

# Load the data of our clean file into newly generated table.

t4 = MySqlOperator(task_id='insert_into_table', mysql_conn_id="mysql_conn", sql="insert_into_table.sql", dag=dag)


# apply some aggregations on our table to fetch the desired information
# Per Client Requirements : We have to generate 2 reports. Once was daily profit, location wise.
# And also, the daily profit of each store.

t5 = MySqlOperator(task_id='select_from_table', mysql_conn_id="mysql_conn", sql="select_from_table.sql", dag=dag)

t6 = BashOperator(task_id='move_file1', bash_command='cat ~/store_files_airflow/location_wise_profit.csv && mv ~/store_files_airflow/location_wise_profit.csv ~/store_files_airflow/location_wise_profit_%s.csv' % yesterday_date, dag=dag)

t7 = BashOperator(task_id='move_file2', bash_command='cat ~/store_files_airflow/store_wise_profit.csv && mv ~/store_files_airflow/store_wise_profit.csv ~/store_files_airflow/store_wise_profit_%s.csv' % yesterday_date, dag=dag)

t8 = EmailOperator(task_id='send_email',
        to='oyinn@outlook.com',
        subject='Daily report generated',
        html_content=""" <h1>Congratulations! Your store reports are ready.</h1> """,
        files=['/usr/local/airflow/store_files_airflow/location_wise_profit_%s.csv' % yesterday_date, '/usr/local/airflow/store_files_airflow/store_wise_profit_%s.csv' % yesterday_date], dag=dag)

t9 = BashOperator(task_id='rename_raw', bash_command='mv ~/store_files_airflow/raw_store_transactions.csv ~/store_files_airflow/raw_store_transactions_%s.csv' % yesterday_date, dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> [t6,t7] >> t8 >> t9

