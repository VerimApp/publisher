import os


TIMEZONE = os.environ.get("TIMEZONE")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DATABASE_URL = os.environ.get("DATABASE_URL")

TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

AUTH_GRPC_HOST = os.environ.get("AUTH_GRPC_HOST")
AUTH_GRPC_PORT = os.environ.get("AUTH_GRPC_PORT")

PUBLISHER_GRPC_SERVER_HOST = os.environ.get("PUBLISHER_GRPC_SERVER_HOST")
PUBLISHER_GRPC_SERVER_PORT = os.environ.get("PUBLISHER_GRPC_SERVER_PORT")

PAGINATION_DEFAULT_PAGE_SIZE = os.environ.get("PAGINATION_DEFAULT_PAGE_SIZE", 20)
PAGINATION_DEFAULT_PAGE = os.environ.get("PAGINATION_DEFAULT_PAGE", 1)

APP_NAME = os.environ.get("PUBLISHER_APP_NAME")
PORT = os.environ.get("PUBLISHER_PORT")
APP_VERSION = os.environ.get("APP_VERSION")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
DEBUG = bool(int(os.environ.get("DEBUG", 0)))

LOGGING_MAX_BYTES = int(os.environ.get("LOGGING_MAX_BYTES"))
LOGGING_BACKUP_COUNT = int(os.environ.get("LOGGING_BACKUP_COUNT"))
LOGGING_LOGGERS = os.environ.get("LOGGING_PUBLISHER_LOGGERS").split(",")
LOGGING_SENSITIVE_FIELDS = os.environ.get("LOGGING_AUTH_SENSITIVE_FIELDS").split(",")
LOG_PATH = os.environ.get("LOGGING_PUBLISHER_PATH")
