import logging
import pickle as pkl
import traceback
import typing as t

from sarus_data_spec import typing as st
from sarus_data_spec.constants import SCALAR_TASK, ScalarCaching
from sarus_data_spec.manager.asyncio.worker.cache_scalar_computation import (
    CacheScalarComputation,
)
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    TypedWorkerManager,
    WorkerComputation,
)
from sarus_data_spec.scalar import Scalar
import sarus_data_spec.protobuf as sp
import sarus_data_spec.status as stt

logger = logging.getLogger(__name__)


class ValueComputation(WorkerComputation[t.Any]):
    """Class responsible for handling the computation
    of scalars."""

    task_name = SCALAR_TASK

    def __init__(
        self,
        manager: TypedWorkerManager,
        cache_scalar_computation: CacheScalarComputation,
    ) -> None:
        super().__init__(manager)
        self.cache_scalar_computation = cache_scalar_computation

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
            except Exception as e:
                stt.error(
                    dataspec=dataspec,
                    manager=self.manager(),
                    task=self.task_name,
                    properties={
                        "message": traceback.format_exc(),
                        'relaunch': str(True),
                    },
                )
                stt.error(
                    dataspec=dataspec,
                    manager=self.manager(),
                    task=self.cache_scalar_computation.task_name,
                    properties={
                        "message": traceback.format_exc(),
                        'relaunch': str(True),
                    },
                )

                raise stt.DataSpecErrorStatus(
                    (True, traceback.format_exc())
                ) from e
            else:
                return data

        return await self.manager().async_value_op(
            scalar=t.cast(Scalar, dataspec)
        )

    async def prepare(self, dataspec: st.DataSpec) -> None:
        try:
            logger.debug(f'STARTED SCALAR {dataspec.uuid()}')

            if self.manager().is_cached(dataspec):
                await self.cache_scalar_computation.task_result(dataspec)
            else:
                await self.manager().async_prepare_parents(dataspec)
        except stt.DataSpecErrorStatus as exception:
            stt.error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    'relaunch': str(exception.relaunch),
                },
            )
            raise
        except Exception:
            stt.error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    'relaunch': str(False),
                },
            )
            raise stt.DataSpecErrorStatus((False, traceback.format_exc()))
        else:
            logging.debug(f'FINISHED SCALAR {dataspec.uuid()}')
            stt.ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
            )
