pre-commit-init:
	poetry run pre-commit install

pre-commit:
	poetry run pre-commit run --all-files

black:
	poetry run black airflow_dag_unittests/

pylint:
	poetry run pylint airflow_dag_unittests/

mypy:
	poetry run mypy airflow_dag_unittests/

test:
	poetry run pytest -vvs tests/

check: black mypy pylint test

airflow:
	docker-compose up -d airflow-init

deploy-local:
	cp -r airflow_dag_unittests* dags/
	mkdir -p dags/airflow_dag_unittests/docs
	cp -r README.md dags/airflow_dag_unittests/docs/

delete-dag:
	rm -rf dags/airflow_dag_unittests
