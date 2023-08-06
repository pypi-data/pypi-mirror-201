import logging
import os

from dotenv import load_dotenv

PACKAGE_PATH = os.path.dirname(__file__)

load_dotenv(override=True)

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# FHIR

FHIR_API_URL = os.environ.get("FHIR_API_URL", "http://localhost:8080/fhir")
FHIR_API_USER = os.environ.get("FHIR_API_USER")
FHIR_API_PASSWORD = os.environ.get("FHIR_API_PASSWORD")
FHIR_COLUMN_NAME = "fhir"
DBT_SCHEMA = "dbt"
FHIR_DBT_SCHEMA = f"{DBT_SCHEMA}_fhir"

# Postgres

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "secret")
POSTGRES_SERVER_NAME = os.environ.get("POSTGRES_SERVER_NAME", "postgres")

SELF_SIGNED_CERTIFICATE_PATH = os.environ.get("SELF_SIGNED_CERTIFICATE_PATH", "")
