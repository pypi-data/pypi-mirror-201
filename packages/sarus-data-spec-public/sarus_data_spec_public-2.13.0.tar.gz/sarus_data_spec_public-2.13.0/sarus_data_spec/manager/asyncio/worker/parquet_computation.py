import logging
import os
import traceback
import typing as t

import pyarrow as pa
import pyarrow.parquet as pq

from sarus_data_spec import typing as st
from sarus_data_spec.constants import CACHE_PATH, TO_PARQUET_TASK
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    WorkerComputation,
)
from sarus_data_spec.status import DataSpecErrorStatus, error, ready

logger = logging.getLogger(__name__)

BATCH_SIZE = 10000


class ToParquetComputation(WorkerComputation[str]):
    """Class responsible for handling the caching
    in parquet of a dataset. It wraps a ToArrowComputation
    to get the iterator."""

    task_name = TO_PARQUET_TASK

    async def prepare(self, dataspec: st.DataSpec) -> None:
        logger.debug(f'STARTING TO_PARQUET {dataspec.uuid()}')
        try:
            iterator = await self.manager().async_to_arrow_op(
                dataset=t.cast(Dataset, dataspec), batch_size=BATCH_SIZE
            )
            batches = [batch async for batch in iterator]
            pq.write_table(
                table=pa.Table.from_batches(batches),
                where=self.cache_path(dataspec=dataspec),
                version='2.6',
            )
        except DataSpecErrorStatus as exception:
            error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    'relaunch': str(exception.relaunch),
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
                    'relaunch': str(False),
                },
            )
            raise DataSpecErrorStatus((False, traceback.format_exc()))
        else:
            logger.debug(f'FINISHED TO_PARQUET {dataspec.uuid()}')
            ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=TO_PARQUET_TASK,
                properties={CACHE_PATH: self.cache_path(dataspec)},
            )

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> str:
        """Returns the cache_path"""
        return properties[CACHE_PATH]

    def cache_path(self, dataspec: st.DataSpec) -> str:
        """Returns the path where to cache the dataset"""
        return os.path.join(
            dataspec.manager().parquet_dir(), f"{dataspec.uuid()}.parquet"
        )
