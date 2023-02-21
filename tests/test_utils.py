import unittest
from airflow_dag_unittests.utils import (
    get_readme_content,
    incr,
)


class test_GetReadmeContent(unittest.TestCase):

    def test_file_exists(self):
        content = get_readme_content("../README.md")
        assert content != ""


    def test_file_does_not_exists(self):
        # with self.assertRaises(Exception) as context:
        #     content = get_readme_content("../<this-files-does-not-exists>")
        # self.assertTrue("No such file or directory" in str(context.exception))
        content = get_readme_content("../<this-files-does-not-exists>")
        assert content == ""


def test_incr():
    assert incr(42) == 43
