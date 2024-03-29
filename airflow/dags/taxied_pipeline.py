from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from datetime import datetime, timedelta

PATH = "/app/source/transformations"
TASK_DEFINITION = "data-pipeline"
CLUSTER_NAME = "my-service"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecs_fargate_dag', default_args=default_args, schedule_interval=timedelta(days=1))

run_bronze_task = EcsRunTaskOperator(
    task_id='run_bronze_task',
    task_definition=TASK_DEFINITION,
    cluster=CLUSTER_NAME,
    overrides={
        'containerOverrides': [{
            'name': 'container_name',
            'command': ['python', f'{PATH}/bronze_taxi_trips_table.py']
        }]
    },
    aws_conn_id='aws_default',
    region_name='us-west-2',
    dag=dag)

run_silver_task = EcsRunTaskOperator(
    task_id='run_silver_task',
    task_definition=TASK_DEFINITION,
    cluster=CLUSTER_NAME,
    overrides={
        'containerOverrides': [{
            'name': 'container_name',
            'command': ['python', f'{PATH}/silver_taxi_trips_table.py']
        }]
    },
    aws_conn_id='aws_default',
    region_name='us-west-2',
    dag=dag)

run_bronze_task >> run_silver_task