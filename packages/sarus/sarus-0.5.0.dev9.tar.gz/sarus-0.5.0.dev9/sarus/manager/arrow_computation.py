import traceback
import typing as t

import pyarrow as pa
import pyarrow.parquet as pq
import sarus_data_spec.status as stt
from sarus_data_spec import typing as st
from sarus_data_spec.constants import ARROW_TASK
from sarus_data_spec.manager.asyncio.api.api_computation import ApiComputation
from sarus_data_spec.manager.asyncio.base import ErrorCatchingAsyncIterator
from sarus_data_spec.manager.asyncio.utils import async_iter

from .caching_computation import ToParquetComputationFromServer
from .dataspec_api import dataset_result, launch_dataspec
from .typing import SDKManager


class ToArrowComputationOnServer(
    ApiComputation[t.AsyncIterator[pa.RecordBatch]]
):
    """ToArrowComputation on the Sarus server through the REST API."""

    task_name = ARROW_TASK

    def __init__(
        self,
        manager: SDKManager,
        parquet_computation: ToParquetComputationFromServer,
    ):
        self._manager: SDKManager = manager
        self.parquet_computation = parquet_computation

    def launch_task(self, dataspec: st.DataSpec) -> None:
        """Launch the computation of a Dataset on the server."""
        status = self.status(dataspec)
        if status is None:
            launch_dataspec(self._manager.client(), dataspec.uuid())
            stt.pending(
                dataspec=dataspec, manager=self.manager(), task=self.task_name
            )

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Return the task result, launch the computation if needed."""
        batch_size = kwargs["batch_size"]

        if self._manager.is_cached(dataspec):
            cache_path = await self.parquet_computation.task_result(dataspec)
            try:
                ait = async_iter(
                    pq.read_table(source=cache_path).to_batches(
                        max_chunksize=batch_size
                    )
                )
            except Exception:
                stt.error(
                    dataspec=dataspec,
                    manager=self.manager(),
                    task=self.task_name,
                    properties={
                        "message": traceback.format_exc(),
                        "relaunch": str(True),
                    },
                )
                stt.error(
                    dataspec=dataspec,
                    manager=self.manager(),
                    task=self.parquet_computation.task_name,
                    properties={
                        "message": traceback.format_exc(),
                        "relaunch": str(True),
                    },
                )
                raise stt.DataSpecErrorStatus((True, traceback.format_exc()))
        else:
            ait = dataset_result(
                self._manager.client(), dataspec.uuid(), batch_size
            )
        return ErrorCatchingAsyncIterator(ait, dataspec, self)
