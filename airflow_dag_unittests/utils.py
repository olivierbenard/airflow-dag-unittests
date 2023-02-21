"""
Module gathering a couple of functions used by the DAGs.
"""
from pathlib import Path


PROJECT_REMOTE_MODULE_PATH = Path(__file__).parent.absolute()
# returns "opt/airflow/dags/your-project" when deployed on local AF instance


def get_readme_content(rel_path: str = "docs/README.md") -> str:
    """
    Method locating the project's README.md under the deployed dags/ folder.
    """

    absolute_path = f"{PROJECT_REMOTE_MODULE_PATH}/{rel_path}"
    content = ""
    try:
        with open(absolute_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        pass  # usually, avoid silencing errors
    return content


def incr(number: float) -> float:
    """
    Take a number an increment it by 1.
    """
    return number + 1
