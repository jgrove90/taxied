from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from datetime import datetime, timedelta

PATH = "/app/src/transformations"
TASK_DEFINITION = "data_pipeline_task"
CLUSTER_NAME = "data_pipeline"
CONTAINER_NAME = "taxied"
PRIVATE_SUBNET_ID = "subnet-0f72e85b0e3d7c6c5"
SECURITY_GROUP_ID = "sg-0f73ac2e35efccac9"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ecs_fargate_dag', 
    default_args=default_args, 
    schedule_interval=timedelta(days=1),
    max_active_runs=1,
    )

network_config = {
    'awsvpcConfiguration': {
        'subnets': [PRIVATE_SUBNET_ID],
        'assignPublicIp': 'DISABLED',
        'securityGroups': [SECURITY_GROUP_ID]
    }
}

run_bronze_task = EcsRunTaskOperator(
    task_id='run_bronze_task',
    task_definition=TASK_DEFINITION,
    cluster=CLUSTER_NAME,
    launch_type='FARGATE',
    overrides={
        'containerOverrides': [{
            'name': CONTAINER_NAME,
            'command': ['python', f'{PATH}/bronze/bronze_taxi_trips_table.py']
        }]
    },
    network_configuration=network_config,
    aws_conn_id='aws_default',
    region_name='us-west-2',
    dag=dag)

run_silver_task = EcsRunTaskOperator(
    task_id='run_silver_task',
    task_definition=TASK_DEFINITION,
    cluster=CLUSTER_NAME,
    launch_type='FARGATE',
    overrides={
        'containerOverrides': [{
            'name': CONTAINER_NAME,
            'command': ['python', f'{PATH}/silver/silver_taxi_trips_table.py']
        }]
    },
    network_configuration=network_config,
    aws_conn_id='aws_default',
    region_name='us-west-2',
    dag=dag)

run_bronze_task >> run_silver_task