from typing import Iterator

import fire
from colorama import Fore, deinit, init
from psycopg2 import ProgrammingError, connect, sql
from psycopg2.extras import RealDictCursor
from requests import HTTPError

from fhir_cli import (
    FHIR_COLUMN_NAME,
    FHIR_DBT_SCHEMA,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    log,
)
from fhir_cli.fhir_resource import FhirResource, FhirValidationError
from utils.compact import dict_compact
from utils.dotty import dotty_dict
from utils.number_print import number_print

CURSOR_ITERSIZE = 20


def get_fhir_resources_from_model(
    cursor, model: str, offset: int = 0, limit: int = 100
) -> Iterator[dict]:
    """get_fhir_resources_from_model looks for a fhir model file and retrieves the Fhir resources

    This function uses a named cursor fetching at most CURSOR_ITERSIZE rows
    at each network roundtrip during iteration on the cursor
    https://www.psycopg.org/docs/cursor.html#cursor.itersize

    Args:
        cursor: a database connection cursor
        model (str): a Fhir model name
        offset (:obj:`int`, optional): an offset for the executed query. Defaults to 0.
        limit (:obj:`int`, optional): a limit for the executed query. Defaults to 100.
    """
    select_fhir_stmt = sql.SQL(
        "SELECT {fhir_column_name} FROM {fhir_model} LIMIT %s OFFSET %s"
    ).format(
        fhir_column_name=sql.Identifier(FHIR_COLUMN_NAME),
        fhir_model=sql.Identifier(model),
    )
    cursor.execute(select_fhir_stmt, (limit, offset))
    for row in cursor:
        yield dotty_dict(dict_compact(row[FHIR_COLUMN_NAME]))


class Cli:
    """a cli to manage your DbtOnFhir project"""

    @staticmethod
    def validate(model: str, schema: str = "", offset: int = 0, limit: int = 100):
        """Extract a fhir model row and validates the Fhir resource
        against a Fhir server

        Args:
            model (str): should be a valid DBT Fhir model name such as `observation_heartrate`
            schema (str): specify the search path
            offset (:obj:`int`, optional): set an offset to the query. Defaults to 0.
            limit (:obj:`int`, optional): a limit for the executed query. Defaults to 100.
        """
        conn = connect(
            host=POSTGRES_HOST,
            dbname=POSTGRES_DB,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            cursor_factory=RealDictCursor,
            options=f"-c search_path={schema or FHIR_DBT_SCHEMA}",
        )
        cursor = conn.cursor(name="curname")
        try:
            # Function in order to filter ANSI escape sequences on Windows
            # see https://pypi.org/project/colorama/
            init(autoreset=True)
            with conn:
                with cursor:
                    cursor.itersize = CURSOR_ITERSIZE
                    for resource in get_fhir_resources_from_model(cursor, model, offset, limit):
                        fhir = FhirResource(resource)
                        number_print(repr(fhir))
                        try:
                            fhir.validate()
                            # The message will be printed in GREEN, hence the weird sequence
                            # at the beginning and at the end
                            log.info(f"{Fore.GREEN}✅ FHIR resource is valid")
                        except FhirValidationError as e:
                            # Same as above
                            log.error(f"{Fore.RED}❌ FHIR resource is not valid\n{e}")
                        input("Press [Return] for the next result or [Ctrl+c] to quit")
        except (ProgrammingError, HTTPError) as e:
            log.error(e)
        except KeyboardInterrupt:
            pass
        finally:
            conn.close()
            # Stop using Colorama
            # see https://pypi.org/project/colorama/
            deinit()


def run():
    cli = Cli()
    fire.Fire(cli)


if __name__ == "__main__":
    run()
