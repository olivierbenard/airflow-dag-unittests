# airflow-dag-unittests

This repo provides a template to demonstrate how to test your Airflow DAGs locally with unittests.

This codebase is related to the following article: [Test Airflow DAG locally](https://olivierbenard.fr/test-airflow-dag-locally).

On top of this, this repo is also provisioning a local Airflow instances so you can test your DAG codebase in a real production-like environment.

You will learn:

1. How to test locally your Airflow DAGs with pytest
2. How to spin-up an Airflow instance locally

## Requirements

This repository uses [poetry](https://olivierbenard.fr/use-poetry-as-python-package-manager/) as Python package manager. You must install it first.

Then, install the dependencies as stated in the `pyproject.toml` file:

    poetry install

You also need to have Docker Desktop up-and-running on your local environment.

## Test your DAG

Simply run the pytest tests:

    make test

You may also want to run the full checks - including black, mypy, pylint and pytest:

    make check

## [Extra] Deploy a DAG on a local Airflow instance

This section provides information on how to deploy your DAG on a local Airflow instance, running on your local environment, using a Docker container.

Before pushing your DAG to Airflow, you need to have an Airflow instance running. Then, you can deploy your code to the dags/ folder of this running Airflow instance.

### Spin-up Airflow

1. The `docker-compose.yaml` file is already provisioned. You may also want to download it:

        curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.2/docker-compose.yaml'

2. Add necessary variables for the Airflow environment:

        echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

3. Compose the Airflow image and run the container:

        make airflow-init

Once started, Airflow's UI can be accessed via: [http://localhost:8080/](http://localhost:8080/)

The credentials are the classic "admin" for both the username and the password.

**Note:** this operation will automatically create additional folders on this repository; mainly logs/ and plugins/. They may contain relevant information but let's just skip this for now.

### Deploy your DAG on Airflow

Because this repository is also provisioning the local airflow instance (somehow you can decouple this and have two repositories instead), you can directly write your DAGs within the `dags/` folder without any extra steps involved.

Traditionally though, you will have to copy your DAGs (as the form of python files), from the repo holding them to the dags/ folder of the repo provisioning the Airflow instance.

In our use-case, this is done by copying the `*.py` files from `airflow_dag_unittests/` to the `dags/` folder:

    make deploy-local

However, should your Airflow instance be spinning in the Cloud - sitting on a Cloud Vendor Service like [Cloud Composer](https://cloud.google.com/composer) for Google Cloud Platform - it would be a different process. In that case, you want to provision it using Terraform (Infrastructure as Code) with an equivalent `sync_dags.tf` file:

```tf
locals {
    dags = toset([
        for file in fileset("${var.root_dir}/../../dags/", "**"):
            file if length(regexall(".*__pycache__.*", file)) == 0
    ])
    code = toset([
        for file in fileset("${var.root_dir}/../../airflow_dag_unittests/", "**"):
            file if length(regexall(".*__pycache__.*", file)) == 0
    ])
    upload_folder = replace(var.service_name, "-", "_")
}

data "google_secret_manager_secret_version" "airflow_bucket" {
  secret = "airflow-bucket-name"
  project = var.project
}
 
resource "google_storage_bucket_object" "dags" {
    for_each = local.dags
    name   = "dags/${local.upload_folder}/${each.key}"
    source = "${var.root_dir}/../../dags/${each.key}"
    bucket = data.google_secret_manager_secret_version.airflow_bucket.secret_data
}
 
resource "google_storage_bucket_object" "code" {
    for_each = local.code
    name   = "dags/${local.upload_folder}/${each.key}"
    source = "${var.root_dir}/../../airflow_dag_unittests/${each.key}"
    bucket = data.google_secret_manager_secret_version.airflow_bucket.secret_data
}  

resource "google_storage_bucket_object" "readme" {
    name   = "dags/${local.upload_folder}/docs/README.md"
    source = "${var.root_dir}/../../README.md"
    bucket = data.google_secret_manager_secret_version.airflow_bucket.secret_data
}
```

## Troubleshooting

Your current Airflow instance is currently stateless. You may want to [set up a database](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html).

This database can retains Airflow variables and connections you can see listed here:

* http://localhost:8080/variable/list/
* http://localhost:8080/connection/list/

You can then read those variables in your codebase, using:

```python
from airfow.models import Variables
variable = Variable.get("your-variable")
```

**Note:** it would be better to use Jinja templated variables when the templated fields allow it.

You might need to reset your Airflow database should you stumble across a similar error:

    ValueError: No such constraint: 'dag_tag__fkey'
  
This is done using:

    poetry run airflow db reset
    poetry run airflow db init

This because it uses a global airflow db instance; on my system:

    DB: sqlite:////Users/<user>/airflow/airflow.db

You might have to reset it e.g. if you have run 'airflow db init' in another project:

    poetry run airflow db reset
    poetry run airflow db init

You might need to mock the variables your code tries to access while executing the pytests should you be confronted to this error:

    KeyError: 'Variable MY_VARIABLE does not exist'

This is done using `@catch.dict()` as you can see [here](https://github.com/olivierbenard/airflow-dag-unittests/blob/main/tests/test_dag.py#L14).
