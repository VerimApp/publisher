import subprocess

from sqlalchemy.sql import text

from config.di import get_di_test_container
from models import mapper_registry


container = get_di_test_container()


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    subprocess.call(["alembic", "-n", "alembic.test", "upgrade", "head"])


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    with container.db().session() as session:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            session.execute(text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE;"))
            session.commit()
