import logging
import traceback

import pyarrow as pa
import pyarrow.parquet as pq
from sarus_data_spec import typing as st
from sarus_data_spec.constants import CACHE_PATH, TO_PARQUET_TASK
from sarus_data_spec.manager.asyncio.worker.caching_computation import (
    ToParquetComputation,
)
from sarus_data_spec.status import DataSpecErrorStatus, error, ready

from .dataspec_api import dataset_result

logger = logging.getLogger(__name__)

BATCH_SIZE = 10000


class ToParquetComputationFromServer(ToParquetComputation):
    """Class responsible for handling the caching
    in parquet of a dataset computed on the server."""

    async def prepare(self, dataspec: st.DataSpec) -> None:

        logger.debug(f"STARTING TO_PARQUET {dataspec.uuid()}")
        try:
            # This task is normally prepared only when the dataset result is
            # ready on the server
            # This line is the only one that changes from the Worker
            # ToParquetComputation
            ait = dataset_result(
                self._manager.client(), dataspec.uuid(), BATCH_SIZE
            )
            batches = [batch async for batch in ait]
            pq.write_table(
                table=pa.Table.from_batches(batches),
                where=self.cache_path(dataspec=dataspec),
                version="2.6",
            )
        except DataSpecErrorStatus as exception:
            error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(exception.relaunch),
                },
            )
            raise DataSpecErrorStatus(
                (exception.relaunch, traceback.format_exc())
            )
        except Exception:
            error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(False),
                },
            )
            raise DataSpecErrorStatus((False, traceback.format_exc()))
        else:
            logger.debug(f"FINISHED TO_PARQUET {dataspec.uuid()}")
            ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=TO_PARQUET_TASK,
                properties={CACHE_PATH: self.cache_path(dataspec)},
            )
