import unittest
from pathlib import Path
from airflow.models import DagBag
from unittest.mock import patch
import pytest


SCRIPT_DIRECTORY = Path(__file__).parent

@pytest.mark.filterwarnings("ignore")
@pytest.fixture(scope="class")
@patch.dict(
    "os.environ",
    AIRFLOW_VAR_YOUR_VARIABLE="", # should you use remote variable, you can mock them here, prefixed with AIRFLOW_VAR.
)
def dag_bag_class(request):
    # set a class attribute on the invoking test context
    request.cls.dag_bag = DagBag(
        dag_folder=SCRIPT_DIRECTORY / ".." / "airflow_dag_unittests",
        read_dags_from_db=False,
    )


@pytest.mark.usefixtures("dag_bag_class")
class test_DAG(unittest.TestCase):

    def test_dag_tasks_count(self):
        dag = self.dag_bag.get_dag(dag_id="airflow-example-unittest")
        assert dag.task_count == 2 # "task_1" and "task_2"

    def test_dags_import_errors(self): # fixture parameter
        assert self.dag_bag.import_errors == {}
