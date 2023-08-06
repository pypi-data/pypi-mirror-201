from __future__ import annotations

import asyncio
import logging
import os
import traceback
import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.manager.asyncio.utils import sync, sync_iterator
from sarus_data_spec.manager.base import Base
from sarus_data_spec.manager.ops.asyncio.processor.external.external_op import (  # noqa: E501
    async_compute_external_value,
)
from sarus_data_spec.manager.typing import Computation, Manager
from sarus_data_spec.schema import Schema
import sarus_data_spec.protobuf as sp
import sarus_data_spec.status as stt
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.bounds import Bounds
    from sarus_data_spec.links import Links
    from sarus_data_spec.marginals import Marginals
    from sarus_data_spec.size import Size

except ModuleNotFoundError:
    pass
try:
    import tensorflow as tf

    from sarus_data_spec.manager.ops.asyncio.tensorflow.features import (
        deserialize,
        flatten,
        nest,
        serialize,
        to_internal_signature,
    )
    from sarus_data_spec.manager.ops.asyncio.tensorflow.tensorflow_visitor import (  # noqa: E501
        convert_tensorflow,
    )
except ModuleNotFoundError:
    pass  # error message printed from typing.py


logger = logging.getLogger(__name__)

BATCH_SIZE = 10000


class BaseAsyncManager(Base):
    """Asynchronous Manager Base implementation
    Make synchronous methods rely on asynchronous ones for consistency.
    """

    def dataspec_computation(self, dataspec: st.DataSpec) -> Computation:
        """Return the Computation for getting the dataspec's value. If sql is
        is true, the sqlcomputation will be returned.
        """
        raise NotImplementedError

    def sql_computation(self) -> Computation:
        """Returns the SQL Computation of the manager. The aim of the method is
        is to reduce code duplication between API and Worker manager
        """
        raise NotImplementedError

    def prepare(self, dataspec: st.DataSpec) -> None:
        """Make sure a Dataspec is ready."""
        sync(self.async_prepare(dataspec))

    async def async_prepare(self, dataspec: st.DataSpec) -> None:
        """Make sure a Dataspec is ready asynchronously."""
        computation = self.dataspec_computation(dataspec)
        await computation.complete_task(dataspec)

    async def async_prepare_parents(self, dataspec: st.DataSpec) -> None:
        """Prepare all the parents of a Dataspec."""
        args, kwargs = dataspec.parents()
        parents = list(args) + list(kwargs.values())
        coros = [self.async_prepare(parent) for parent in parents]
        # here, if many parents potentially fail, we want to be sure
        # that all of them do it, and not only the first one (to
        # modify all statuses accordingly).
        # After, we only raise the first exception for the child.

        results = await asyncio.gather(*coros, return_exceptions=True)
        exceptions = [
            element for element in results if isinstance(element, Exception)
        ]
        if len(exceptions) == 0:
            return
        raise error_aggregation(exceptions)

    async def async_value(self, scalar: st.Scalar) -> t.Any:
        """Reads asynchronously value of a scalar."""
        computation = self.dataspec_computation(scalar)
        return await computation.task_result(dataspec=scalar)

    def value(self, scalar: st.Scalar) -> st.DataSpecValue:
        return sync(self.async_value(scalar=scalar))

    async def async_to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Reads asynchronous iterator of datast batches"""
        computation = t.cast(
            BaseComputation[t.AsyncIterator[pa.RecordBatch]],
            self.dataspec_computation(dataset),
        )
        return await computation.task_result(
            dataspec=dataset, batch_size=batch_size
        )

    def to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.Iterator[pa.RecordBatch]:
        return sync_iterator(
            self.async_to_arrow(dataset=dataset, batch_size=batch_size)
        )

    async def async_to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        batches_async_it = await self.async_to_arrow(
            dataset=dataset, batch_size=BATCH_SIZE
        )
        arrow_batches = [batch async for batch in batches_async_it]
        return pa.Table.from_batches(arrow_batches).to_pandas()

    def to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        return sync(self.async_to_pandas(dataset=dataset))

    def to_tensorflow(self, dataset: st.Dataset) -> tf.data.Dataset:
        return sync(self.async_to_tensorflow(dataset=dataset))

    def schema(self, dataset: st.Dataset) -> Schema:
        return t.cast(Schema, sync(self.async_schema(dataset=dataset)))

    def to_parquet(self, dataset: st.Dataset) -> None:
        sync(self.async_to_parquet(dataset=dataset))

    def to_sql(self, dataset: st.Dataset) -> None:
        sync(self.async_to_sql(dataset=dataset))

    def sql_prepare(self, dataset: st.Dataset) -> None:
        """SQL prepare dataset."""
        sync(self.async_sql_prepare(dataset))

    async def async_sql_prepare(self, dataset: st.Dataset) -> None:
        """SQL prepare the dataset synchronously"""
        computation = t.cast(
            BaseComputation[t.AsyncIterator[pa.RecordBatch]],
            self.sql_computation(),
        )
        await computation.complete_task(dataset)

    async def async_sql_prepare_parents(self, dataset: st.Dataset) -> None:
        """SQL prepare all the parents of a dataset: calling async_sql_prepare
        for dataset parents and async_prepare for scalar parents.
        """
        args, kwargs = dataset.parents()
        parents = list(args) + list(kwargs.values())
        coros = [
            self.async_sql_prepare(t.cast(st.Dataset, parent))
            if dataset.prototype() == sp.Dataset
            else self.async_prepare(parent)
            for parent in parents
        ]
        # here, if many parents potentially fail, we want to be sure
        # that all of them do it, and not only the first one (to
        # modify all statuses accordingly).
        # After, we only raise the first exception for the child.

        results = await asyncio.gather(*coros, return_exceptions=True)
        exceptions = [
            element for element in results if isinstance(element, Exception)
        ]
        if len(exceptions) == 0:
            return
        raise error_aggregation(exceptions)

    def sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Mapping[t.Union[str, t.Tuple[str, ...]], str]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> t.Iterator[pa.RecordBatch]:
        return sync_iterator(
            self.async_sql(dataset, query, dialect, batch_size)
        )

    async def async_sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Mapping[t.Union[str, t.Tuple[str, ...]], str]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        computation = t.cast(
            BaseComputation[t.AsyncIterator[pa.RecordBatch]],
            self.sql_computation(),
        )
        return await computation.task_result(
            dataset, query=query, dialect=dialect, batch_size=batch_size
        )

    def cache_scalar(self, scalar: st.Scalar) -> None:
        sync(self.async_cache_scalar(scalar=scalar))

    def size(self, dataset: st.Dataset) -> st.Size:
        return t.cast(Size, sync(self.async_size(dataset)))

    def bounds(self, dataset: st.Dataset) -> st.Bounds:
        return t.cast(Bounds, sync(self.async_bounds(dataset)))

    def marginals(self, dataset: st.Dataset) -> st.Marginals:
        return t.cast(Marginals, sync(self.async_marginals(dataset)))

    def links(self, dataset: st.Dataset) -> st.Links:
        return t.cast(Links, sync(self.async_links(dataset)))

    def foreign_keys(self, dataset: st.Dataset) -> t.Dict[st.Path, st.Path]:
        return t.cast(
            t.Dict[st.Path, st.Path], sync(self.async_foreign_keys(dataset))
        )

    def primary_keys(self, dataset: st.Dataset) -> t.List[st.Path]:
        return t.cast(t.List[st.Path], sync(self.async_primary_keys(dataset)))

    async def async_links(self, dataset: st.Dataset) -> t.Any:
        raise NotImplementedError

    async def async_to_tensorflow(
        self, dataset: st.Dataset
    ) -> tf.data.Dataset:
        root_dir = os.path.join(
            self.parquet_dir(), "tfrecords", dataset.uuid()
        )
        schema_type = (await self.async_schema(dataset)).type()
        signature = to_internal_signature(schema_type)

        if not os.path.exists(root_dir):
            # the dataset is cached first
            os.makedirs(root_dir)

            flattener = flatten(signature)
            serializer = serialize(signature)
            i = 0
            batches_async_it = await self.async_to_arrow(
                dataset=dataset, batch_size=BATCH_SIZE
            )
            async for batch in batches_async_it:
                filename = os.path.join(root_dir, f"batch_{i}.tfrecord")
                i += 1
                await write_tf_batch(
                    filename, batch, schema_type, flattener, serializer
                )

        # reading from cache
        glob = os.path.join(root_dir, "*.tfrecord")
        filenames = tf.data.Dataset.list_files(glob, shuffle=False)
        deserializer = deserialize(signature)
        nester = nest(signature)
        return tf.data.TFRecordDataset(filenames).map(deserializer).map(nester)

    def mock_value(
        self,
        transform: st.Transform,
        *arguments: st.DataSpec,
        **named_arguments: st.DataSpec,
    ) -> t.Any:
        """Compute the mock value of an external transform applied on
        Dataspecs.
        """
        assert transform.is_external()
        mock_args = [arg.variant(st.ConstraintKind.MOCK) for arg in arguments]
        named_mock_args = {
            name: arg.variant(st.ConstraintKind.MOCK)
            for name, arg in named_arguments.items()
        }

        if any([ds is None for ds in mock_args]) or any(
            [ds is None for ds in named_mock_args.values()]
        ):
            raise ValueError(
                "Cannot infer the output type of the external "
                "transform because one of the parents has a None MOCK."
            )

        typed_mock_args = [t.cast(st.DataSpec, ds) for ds in mock_args]
        typed_named_mock_args = {
            name: t.cast(st.DataSpec, ds)
            for name, ds in named_mock_args.items()
        }

        try:
            mock_value = sync(
                async_compute_external_value(
                    transform, *typed_mock_args, **typed_named_mock_args
                )
            )
        except Exception as e:
            raise e

        return mock_value


async def write_tf_batch(
    filename: str,
    batch: pa.RecordBatch,
    schema_type: st.Type,
    flattener: t.Callable,
    serializer: t.Callable,
) -> None:
    with tf.io.TFRecordWriter(filename) as writer:
        batch = convert_tensorflow(
            convert_record_batch(record_batch=batch, _type=schema_type),
            schema_type,
        )
        batch = tf.data.Dataset.from_tensor_slices(batch).map(flattener)
        for row in batch:
            as_bytes = serializer(row)
            writer.write(as_bytes)


T = t.TypeVar("T")


class BaseComputation(Computation[T]):
    """General class that implements some
    methods of the protocol shared by all task
    computations"""

    task_name = ''

    def __init__(self, manager: Manager):
        self._manager = manager

    def manager(self) -> Manager:
        return self._manager

    def status(self, dataspec: st.DataSpec) -> t.Optional[st.Status]:
        return self.manager().status(dataspec, self.task_name)

    def launch_task(self, dataspec: st.DataSpec) -> t.Optional[t.Awaitable]:
        """Launch the task computation.

        Returns an optional awaitable that can be used in async functions to
        wait for the task to complete. This can be useful if some managers have
        a more efficient way than statuses to await for the result.
        """
        raise NotImplementedError

    async def task_result(self, dataspec: st.DataSpec, **kwargs: t.Any) -> T:
        """Return the task result.

        This is the main entry point from outide the computation. The call to
        `complete_task` will launch the task if it does not exist and wait for
        it to be ready.

        Here, we assert that the task is ready and then get the result in a
        try/catch block.
        """
        status = await self.complete_task(dataspec=dataspec)
        stage = status.task(self.task_name)
        assert stage
        assert stage.ready()
        try:
            return await self.read_ready_result(
                dataspec, stage.properties(), **kwargs
            )
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

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> T:
        """Return the task result by reading cache or computing the value."""
        raise NotImplementedError

    async def complete_task(self, dataspec: st.DataSpec) -> st.Status:
        """Poll the last status for the given task and if no status
        is available either performs the computation or delegates it
        to another manager. Then keeps polling until either the task
        is completed or an error occurs."""

        manager_status = stt.last_status(
            dataspec=dataspec, manager=self.manager(), task=self.task_name
        )

        if manager_status is None:
            task = self.launch_task(dataspec=dataspec)
            if task is not None:
                # NB: an exception raised in an asyncio task will be reraised
                # in the awaiting code
                await task
            # In the other cases, the complete_task will be reentered with
            # the pending status, resulting in a polling process
            return await self.complete_task(dataspec)

        else:
            last_task = t.cast(st.Stage, manager_status.task(self.task_name))
            if last_task.ready():
                return manager_status
            elif last_task.pending():
                return await self.pending(dataspec)
            elif last_task.processing():
                return await self.processing(dataspec)
            elif last_task.error():
                return await self.error(dataspec)
            else:
                raise ValueError(f"Inconsistent status {manager_status}")

    async def pending(self, dataspec: st.DataSpec) -> st.Status:
        """The behaviour depends on the manager"""
        raise NotImplementedError

    async def processing(self, dataspec: st.DataSpec) -> st.Status:
        """The behaviour depends on the manager"""
        raise NotImplementedError

    async def error(
        self,
        dataspec: st.DataSpec,
    ) -> st.Status:
        """The DataSpec already has an Error status.
        In this case, we clear the statuses so that the
        task can be relaunched in the future.
        """
        status = self.status(dataspec)
        assert status
        stage = status.task(self.task_name)
        assert stage
        should_clear = status_error_policy(stage=stage)
        if should_clear:
            stt.clear_task(dataspec=dataspec, task=self.task_name)
            return await self.complete_task(dataspec=dataspec)
        raise stt.DataSpecErrorStatus(
            (
                stage.properties()["relaunch"] == str(True),
                stage.properties()["message"],
            )
        )

    async def wait_for_computation(
        self,
        dataspec: st.DataSpec,
        current_stage: str,
        timeout: int = 300,
        max_delay: int = 10,
    ) -> st.Stage:
        """Utility to wait for the availability of a computation, by polling
        its status for at most `timeout` seconds, with a period of at most
        `max_delay` seconds between each attempt. Delay grows exponentially
        at first."""
        delay = min(1, timeout, max_delay)
        total_wait = 0
        while total_wait < timeout:
            status = self.status(dataspec=dataspec)
            assert status
            stage = status.task(self.task_name)
            assert stage
            if stage.stage() == current_stage:
                logger.debug(f'POLLING {self.task_name} {dataspec.uuid()}')
                await asyncio.sleep(delay)
                total_wait += delay
                delay = min(2 * delay, max_delay, timeout - total_wait)
            else:
                break
        assert stage
        return stage


class ErrorCatchingAsyncIterator:
    """Wrap an AsyncIterator and catches potential errors.

    When an error occurs, this sets the Dataspec status to error
    accordingly.
    """

    def __init__(
        self,
        ait: t.AsyncIterator,
        dataspec: st.DataSpec,
        computation: BaseComputation,
    ):
        self.ait = ait
        self.computation = computation
        self.dataspec = dataspec
        self.agen: t.Optional[t.AsyncIterator] = None

    def __aiter__(self) -> t.AsyncIterator:
        return self.ait

    async def __anext__(self) -> t.Any:
        try:
            batch = await self.ait.__anext__()
        except StopAsyncIteration:
            raise
        except stt.DataSpecErrorStatus as exception:
            stt.error(
                dataspec=self.dataspec,
                manager=self.computation.manager(),
                task=self.computation.task_name,
                properties={
                    "message": traceback.format_exc(),
                    'relaunch': str(exception.relaunch),
                },
            )
            raise
        except Exception:
            stt.error(
                dataspec=self.dataspec,
                manager=self.computation.manager(),
                task=self.computation.task_name,
                properties={
                    "message": traceback.format_exc(),
                    'relaunch': str(False),
                },
            )
            raise stt.DataSpecErrorStatus((False, traceback.format_exc()))

        else:
            return batch


def status_error_policy(stage: st.Stage) -> bool:
    """This methods returns whether a given error message
    should be reset to None or not. Currently, the quick
    shortcut is to check whether the error message starts
    with a TimeoutError, in this case, we want to retry"""
    assert stage.error()
    return stage.properties().get('relaunch', 'False') == str(True)


def error_aggregation(errors: t.List[Exception]) -> Exception:
    """Takes as input a list of exceptions, the first error
    that is not a DataSpecErrorStatus or that has not a relaunch.
    If they are all DataSpecErrorStatuses with relaunch, returns
    the first"""

    for error in errors:
        if isinstance(error, stt.DataSpecErrorStatus) and error.relaunch:
            continue
        else:
            return error

    return errors[0]
