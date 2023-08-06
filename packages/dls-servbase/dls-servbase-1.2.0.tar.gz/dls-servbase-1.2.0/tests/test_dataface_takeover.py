import logging

from dls_servbase_api.databases.constants import CookieFieldnames, Tablenames

# Object managing datafaces.
from dls_servbase_api.datafaces.datafaces import dls_servbase_datafaces_get_default

# Context creator.
from dls_servbase_lib.contexts.contexts import Contexts
from dls_servbase_lib.datafaces.context import Context as DatafaceContext

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestDatafaceTakeover:
    def test_dataface_laptop(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/servbase.yaml"
        DatafaceTakeoverTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class DatafaceTakeoverTester(BaseContextTester):
    """
    Class to test that a second instance of the dataface will cause the first one to shut down.
    """

    async def _main_coroutine(self, constants, output_directory):
        """ """

        dls_servbase_multiconf = self.get_multiconf()

        context_configuration = await dls_servbase_multiconf.load()
        dls_servbase_context = Contexts().build_object(context_configuration)

        async with dls_servbase_context:
            dataface = dls_servbase_datafaces_get_default()

            # Write one record.
            await dataface.insert(
                Tablenames.COOKIES,
                [
                    {
                        CookieFieldnames.UUID: "f0",
                        CookieFieldnames.CONTENTS: "{'a': 'f000'}",
                    }
                ],
            )

            # Make a new dataface context with the same specification.
            dataface_specification = dls_servbase_multiconf.require(
                "dls_servbase_dataface_specification"
            )

            # Activate the new dataface which should send shutdown to the old process.
            async with DatafaceContext(dataface_specification):
                all_sql = f"SELECT * FROM {Tablenames.COOKIES}"
                records = await dataface.query(all_sql)

                assert len(records) == 1
                assert records[0][CookieFieldnames.UUID] == "f0"
                assert records[0][CookieFieldnames.CONTENTS] == "{'a': 'f000'}"

            # From the top level context's point of view, one of its processs is dead.
            assert await dls_servbase_context.is_any_process_dead()

        assert not await dls_servbase_context.is_any_process_alive()
