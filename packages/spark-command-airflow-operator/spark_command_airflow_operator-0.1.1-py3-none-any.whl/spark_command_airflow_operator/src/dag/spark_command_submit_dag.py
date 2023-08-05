from airflow import DAG
from airflow.utils.dates import days_ago
from spark_command_airflow_operator.src.operator.spark_command_submit_operator import SparkCommandSubmitOperator

with DAG("spark_sql_random",
         schedule_interval='@daily',
         start_date=days_ago(0),
         ) as dag:
    spark_sql_random = SparkCommandSubmitOperator(task_id='random_from_spark',
                                                  name='Spark Random',
                                                  endpoint_url='http://localhost:5000',
                                                  code_type='SQL',
                                                  code='select random()',
                                                  result_type='text',
                                                  result_url='')


