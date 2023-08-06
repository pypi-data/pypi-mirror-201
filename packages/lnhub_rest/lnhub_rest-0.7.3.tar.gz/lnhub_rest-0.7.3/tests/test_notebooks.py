import os
from pathlib import Path

from nbproject._logger import logger
from nbproject.dev import test


def test_notebooks():
    # assuming this is in the tests folder
    docs_folder = Path(__file__).parents[1] / "docs/"

    if os.environ["LAMIN_ENV"] == "local":
        logger.debug("\nmigration")
        test.execute_notebooks(docs_folder / "migration/", write=True)

    logger.debug("\nchecks")
    test.execute_notebooks(docs_folder / "checks/", write=True)

    logger.debug("\naccount")
    test.execute_notebooks(docs_folder / "account/", write=True)

    logger.debug("\ninstance")
    test.execute_notebooks(docs_folder / "instance/", write=True)

    logger.debug("\nstorage")
    test.execute_notebooks(docs_folder / "storage/", write=True)
