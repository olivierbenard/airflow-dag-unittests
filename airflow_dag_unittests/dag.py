"""
Module implementing a DAG performing basic operations.
"""

from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow_dag_unittests.utils import (
    get_readme_content,
    incr,
)

Variable.set("my_variable", value="hello world!")

ARGS = {
    "start_date": days_ago(2),
    "schedule_interval": "1 * * * *",  # set it to None to pause it
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": True,
}

with DAG(
    dag_id="airflow-example-unittest",
    default_args=ARGS,
    description="",
    doc_md=get_readme_content(),
    tags=["playground", "unittest"],
) as dag:
    task_1 = PythonOperator(
        task_id="task_1",
        python_callable=incr,
        op_kwargs={
            "number": 42,
        },
    )

    task_2 = PythonOperator(
        task_id="task_2",
        python_callable=lambda astr: astr.upper(),  # type: ignore[pointless-statement]
        op_args=[Variable.get("my_variable")],
    )

    task_1 >> task_2  # pylint: disable="pointless-statement"
