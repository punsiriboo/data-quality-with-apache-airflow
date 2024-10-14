import pytest
from airflow.models import DagBag

@pytest.fixture
def dagbag():
    return DagBag(dag_folder="./dags/", include_examples=False)

def test_dagbag_load(dagbag):
    assert len(dagbag.dags) > 0

def test_dagbag_no_errors(dagbag):
    assert len(dagbag.import_errors) == 0

def test_dagbag_no_duplicate_dag_ids(dagbag):
    dag_ids = [dag.dag_id for dag in dagbag.dags.values()]
    assert len(dag_ids) == len(set(dag_ids))

def test_dagbag_no_duplicate_task_ids(dagbag):
    for dag in dagbag.dags.values():
        task_ids = [task.task_id for task in dag.tasks]
        assert len(task_ids) == len(set(task_ids))

def test_dagbag_no_invalid_task_types(dagbag):
    for dag in dagbag.dags.values():
        for task in dag.tasks:
            assert task.operator_class is not None

def test_dagbag_no_invalid_task_configs(dagbag):
    for dag in dagbag.dags.values():
        for task in dag.tasks:
            assert task.operator_extra_links is not None

def test_dagbag_no_invalid_task_params(dagbag):
    for dag in dagbag.dags.values():
        for task in dag.tasks:
            assert task.params is not None