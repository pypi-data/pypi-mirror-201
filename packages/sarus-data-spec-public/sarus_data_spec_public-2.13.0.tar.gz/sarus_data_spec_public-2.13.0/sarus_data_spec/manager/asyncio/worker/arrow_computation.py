import logging
import traceback
import typing as t

import pyarrow as pa
import pyarrow.parquet as pq

from sarus_data_spec import typing as st
from sarus_data_spec.constants import ARROW_TASK
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.asyncio.base import ErrorCatchingAsyncIterator
from sarus_data_spec.manager.asyncio.utils import async_iter
from sarus_data_spec.manager.asyncio.worker.caching_computation import (
    ToParquetComputation,
)
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    TypedWorkerManager,
    WorkerComputation,
)
import sarus_data_spec.status as stt

logger = logging.getLogger(__name__)


class ToArrowComputation(WorkerComputation[t.AsyncIterator[pa.RecordBatch]]):
    task_name = ARROW_TASK

    def __init__(
        self,
        manager: TypedWorkerManager,
        parquet_computation: ToParquetComputation,
    ) -> None:
        super().__init__(manager)
        self.parquet_computation = parquet_computation

    async def prepare(self, dataspec: st.DataSpec) -> None:
        try:
            logger.debug(f'STARTED ARROW {dataspec.uuid()}')
            # Only prepare parents since calling `to_arrow` will require the
            # computation of the scalars in the ancestry.
            dataset = t.cast(st.Dataset, dataspec)

            if self.manager().is_cached(dataspec):
                await self.parquet_computation.task_result(dataspec)

            else:
                await self.manager().async_prepare_parents(dataset)
                if dataset.is_source():
                    await self.manager().async_schema(dataset)
                elif dataset.is_transformed():
                    transform = dataset.transform()
                    if not transform.is_external():
                        await self.manager().async_schema(dataset)
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
            logger.debug(f'FINISHED ARROW {dataspec.uuid()}')
            stt.ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
            )

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Returns the iterator"""
        batch_size = kwargs['batch_size']

        if self.manager().is_cached(dataspec):
            status = self.parquet_computation.status(dataspec)
            assert status
            stage = status.task(self.parquet_computation.task_name)
            assert stage
            assert stage.ready()
            cache_path = await self.parquet_computation.read_ready_result(
                dataspec, stage.properties()
            )
            try:
                ait = async_iter(
                    pq.read_table(source=cache_path).to_batches(
                        max_chunksize=batch_size
                    )
                )
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
                    task=self.parquet_computation.task_name,
                    properties={
                        "message": traceback.format_exc(),
                        'relaunch': str(True),
                    },
                )

                raise stt.DataSpecErrorStatus(
                    (True, traceback.format_exc())
                ) from e
        else:
            ait = await self.manager().async_to_arrow_op(
                dataset=t.cast(Dataset, dataspec), batch_size=batch_size
            )
        return ErrorCatchingAsyncIterator(ait, dataspec, self)
