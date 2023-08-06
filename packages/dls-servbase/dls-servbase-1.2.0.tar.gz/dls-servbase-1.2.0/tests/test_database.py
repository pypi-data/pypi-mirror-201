import asyncio
import logging
import multiprocessing

import pytest

from dls_servbase_api.databases.constants import CookieFieldnames, Tablenames
from dls_servbase_lib.databases.databases import Databases

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatabaseSqlite:
    def test(self, constants, logging_setup, output_directory):
        """
        Tests the sqlite implementation of the Database interface.

        This does not use a service.
        """

        database_specification = {
            "type": "dls_servbase_lib.databases.aiosqlite",
            "filename": "%s/dls_servbase_scheduler.sqlite" % (output_directory),
        }

        # Test direct SQL access to the database.
        DatabaseTesterImage().main(
            constants,
            database_specification,
            output_directory,
        )


# ----------------------------------------------------------------------------------------
class _BaseTester:
    """
    Provide asyncio loop and error checking over *Tester classes.
    """

    def main(self, constants, specification, output_directory):
        """
        This is the main program which calls the test using asyncio.
        """

        multiprocessing.current_process().name = "main"

        failure_message = None
        try:
            # Run main test in asyncio event loop.
            asyncio.run(
                self._main_coroutine(constants, specification, output_directory)
            )

        except Exception as exception:
            logger.exception(
                "unexpected exception in the test method", exc_info=exception
            )
            failure_message = str(exception)

        if failure_message is not None:
            pytest.fail(failure_message)


# ----------------------------------------------------------------------------------------
class DatabaseTesterImage(_BaseTester):
    """
    Test direct SQL access to the database.
    """

    async def _main_coroutine(
        self, constants, database_specification, output_directory
    ):
        """ """

        databases = Databases()
        database = databases.build_object(database_specification)

        try:
            # Connect to database.
            await database.connect()

            # Write one record.
            await database.insert(
                Tablenames.COOKIES,
                [
                    {
                        CookieFieldnames.UUID: "f0",
                        CookieFieldnames.CONTENTS: "{'a': 'f000'}",
                    }
                ],
            )
            all_sql = f"SELECT * FROM {Tablenames.COOKIES}"
            records = await database.query(all_sql)
            assert len(records) == 1

            # Bulk insert more records.
            insertable_records = [
                ["f1", "{'a': 'f111'}"],
                ["f2", "{'a': 'f111'}"],
                ["f3", "{'a': 'f111'}"],
                ["f4", "{'a': 'f111'}"],
            ]
            await database.execute(
                f"INSERT INTO {Tablenames.COOKIES}"
                f" ({CookieFieldnames.UUID}, {CookieFieldnames.CONTENTS})"
                " VALUES (?, ?)",
                insertable_records,
            )

            all_sql = f"SELECT * FROM {Tablenames.COOKIES}"
            records = await database.query(all_sql)
            assert len(records) == 5

        finally:
            # Connect from the database... necessary to allow asyncio loop to exit.
            await database.disconnect()
