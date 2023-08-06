import logging
import pickle as pkl
import traceback

import sarus_data_spec.protobuf as sp
from sarus_data_spec import typing as st
from sarus_data_spec.constants import (
    CACHE_PATH,
    CACHE_PROTO,
    CACHE_TYPE,
    ScalarCaching,
)
from sarus_data_spec.manager.asyncio.worker.cache_scalar_computation import (
    CacheScalarComputation,
)
from sarus_data_spec.status import DataSpecErrorStatus, error, ready

from .dataspec_api import scalar_result

logger = logging.getLogger(__name__)


class CacheScalarComputationFromServer(CacheScalarComputation):
    """Class responsible for handling the caching
    in of a scalar computed on the server."""

    async def prepare(self, dataspec: st.DataSpec) -> None:

        logger.debug(f"STARTING CACHE_SCALAR {dataspec.uuid()}")
        try:
            # This task is normally prepared only when the scalar result is
            # ready on the server
            # This line is the only one that changes from the Worker
            # CacheScalarComputation
            value = scalar_result(self._manager.client(), dataspec.uuid())
            if isinstance(value, st.HasProtobuf):
                properties = {
                    CACHE_PROTO: sp.to_base64(value.protobuf()),
                    CACHE_TYPE: sp.type_name(value.prototype()),
                }
            else:
                properties = {
                    CACHE_TYPE: ScalarCaching.PICKLE.value,
                    CACHE_PATH: self.cache_path(dataspec),
                }
                with open(self.cache_path(dataspec), "wb") as f:
                    pkl.dump(value, f)

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
            logger.debug(f"FINISHED CACHE_SCALAR {dataspec.uuid()}")
            ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties=properties,
            )
