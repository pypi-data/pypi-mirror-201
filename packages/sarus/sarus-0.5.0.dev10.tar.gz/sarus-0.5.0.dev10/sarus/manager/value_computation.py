import pickle as pkl
import traceback
import typing as t

import sarus_data_spec.protobuf as sp
import sarus_data_spec.status as stt
from sarus_data_spec import typing as st
from sarus_data_spec.constants import SCALAR_TASK, ScalarCaching
from sarus_data_spec.manager.asyncio.api.api_computation import ApiComputation

from .cache_scalar_computation import CacheScalarComputationFromServer
from .dataspec_api import launch_dataspec, scalar_result
from .typing import SDKManager


class ValueComputationOnServer(ApiComputation[t.Any]):
    """ValueComputation on the Sarus server through the REST API."""

    task_name = SCALAR_TASK

    def __init__(
        self,
        manager: SDKManager,
        cache_scalar_computation: CacheScalarComputationFromServer,
    ):
        self._manager: SDKManager = manager
        self.cache_scalar_computation = cache_scalar_computation

    def launch_task(self, dataspec: st.DataSpec) -> None:
        """Launch the computation of a Scalar on the server."""
        status = self.status(dataspec=dataspec)
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
    ) -> t.Any:
        if self.manager().is_cached(dataspec):
            (
                cache_type,
                cache,
            ) = await self.cache_scalar_computation.task_result(dataspec)
            try:
                if cache_type == ScalarCaching.PICKLE.value:
                    with open(cache, "rb") as f:
                        data = pkl.load(f)

                else:
                    data = sp.python_proto_factory(cache, cache_type)
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
                    task=self.cache_scalar_computation.task_name,
                    properties={
                        "message": traceback.format_exc(),
                        "relaunch": str(True),
                    },
                )
                raise stt.DataSpecErrorStatus((True, traceback.format_exc()))
            else:
                return data

        return await scalar_result(self._manager.client(), dataspec.uuid())
