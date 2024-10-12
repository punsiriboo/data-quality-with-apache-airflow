import airflow
from airflow import AirflowException
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.greatexpectations.operators.greatexpectations import GreatExpectationsOperator

default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='ge_dag',
    default_args=default_args
)

ge_checkpoint_fail = GreatExpectationsOperator(
    task_id='ge_checkpoint_fail',
    run_id='ge_airflow_run',
    checkpoint_name='taxi.fail.chk',
    dag=dag
)

ge_checkpoint_pass = GreatExpectationsOperator(
    task_id='ge_checkpoint_pass',
    run_id='ge_airflow_run',
    checkpoint_name='taxi.pass.chk',
    dag=dag
)

ge_batch_kwargs_pass = GreatExpectationsOperator(
    task_id='ge_batch_kwargs_pass',
    expectation_suite_name='taxi.demo',
    batch_kwargs={
        'path': '/Users/sam/code/ge_demo/data/yellow_tripdata_sample_2019-01.csv',
        'datasource': 'data__dir'
    },
    dag=dag
)

ge_batch_kwargs_list_pass = GreatExpectationsOperator(
    task_id='ge_batch_kwargs_list_pass',
    assets_to_validate=[
        {
            'batch_kwargs': {
                'path': '/Users/sam/code/ge_demo/data/yellow_tripdata_sample_2019-01.csv',
                'datasource': 'data__dir'
            },
            'expectation_suite_name': 'taxi.demo'
        }
    ],
    dag=dag
)

ge_checkpoint_pass_root_dir = GreatExpectationsOperator(
    task_id='ge_checkpoint_pass_root_dir',
    run_id='ge_airflow_run',
    checkpoint_name='taxi.pass.chk',
    data_context_root_dir='/Users/sam/code/ge_demo/great_expectations',
    dag=dag
)

ge_wrong_root_dir = GreatExpectationsOperator(
    task_id='ge_wrong_root_dir',
    run_id='ge_airflow_run',
    checkpoint_name='taxi.pass.chk',
    data_context_root_dir='/Users/sam/code/',
    dag=dag
)

ge_too_many_args = GreatExpectationsOperator(
    task_id='ge_too_many_args',
    run_id='ge_airflow_run',
    checkpoint_name='taxi.pass.chk',
    batch_kwargs={},
    expectation_suite_name='my_suite',
    dag=dag
)

# Create an operator using an in-memory data context from a dictionary
data_context_config = DataContextConfig(
  {
    # the mega dictionary 
  }
)
data_context = BaseDataContext(project_config=data_context_config)

ge_in_memory_context = GreatExpectationsOperator(
    task_id='ge_in_memory_context',
    run_id='ge_airflow_run',
    data_context=data_context,
    dag=dag
)