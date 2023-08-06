from __future__ import annotations

import hashlib
import os
import typing as t
import warnings

import pandas as pd
import pyarrow as pa

try:
    import tensorflow as tf
except ModuleNotFoundError:
    pass  # Warning is displayed by typing.py

from uuid import UUID

from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.constants import (
    BIG_DATA_TASK,
    BIG_DATA_THRESHOLD,
    DATASET_N_BYTES,
    DATASET_N_LINES,
    DATASET_TYPES,
    IS_BIG_DATA,
    IS_REMOTE,
    THRESHOLD_TYPE,
)
from sarus_data_spec.dataspec_rewriter.base import BaseDataspecRewriter
from sarus_data_spec.dataspec_validator.base import BaseDataspecValidator
from sarus_data_spec.protobuf.utilities import copy
from sarus_data_spec.protobuf.utilities import json as utilities_json
from sarus_data_spec.protobuf.utilities import serialize, type_name
from sarus_data_spec.scalar import Scalar
import sarus_data_spec.dataspec_rewriter.typing as sdrt
import sarus_data_spec.dataspec_validator.typing as sdvt
import sarus_data_spec.manager.typing as manager_typing
import sarus_data_spec.protobuf as sp
import sarus_data_spec.status as stt
import sarus_data_spec.storage.typing as storage_typing
import sarus_data_spec.typing as st


class Base(manager_typing.Manager):
    """Provide the dataset functionalities."""

    def __init__(
        self, storage: storage_typing.Storage, protobuf: sp.Manager
    ) -> None:
        self._protobuf: sp.Manager = copy(protobuf)
        self._freeze()
        self._storage = storage
        self.storage().store(self)
        self._parquet_dir = os.path.expanduser('/tmp/sarus_dataset/')
        os.makedirs(self.parquet_dir(), exist_ok=True)
        self._dataspec_rewriter = BaseDataspecRewriter(storage=storage)
        self._dataspec_validator = BaseDataspecValidator(storage=storage)

    def dataspec_rewriter(self) -> sdrt.DataspecRewriter:
        return self._dataspec_rewriter

    def dataspec_validator(self) -> sdvt.DataspecValidator:
        return self._dataspec_validator

    def parquet_dir(self) -> str:
        return self._parquet_dir

    def protobuf(self) -> sp.Manager:
        return copy(self._protobuf)

    def prototype(self) -> t.Type[sp.Manager]:
        return sp.Manager

    def type_name(self) -> str:
        return type_name(self._protobuf)

    def __repr__(self) -> str:
        return utilities_json(self._protobuf)

    def __getitem__(self, key: str) -> str:
        return t.cast(str, self._protobuf.properties[key])

    def properties(self) -> t.Mapping[str, str]:
        return self.protobuf().properties

    def _checksum(self) -> bytes:
        """Compute an md5 checksum"""
        md5 = hashlib.md5()
        md5.update(serialize(self._protobuf))
        return md5.digest()

    def _freeze(self) -> None:
        self._protobuf.uuid = ''
        self._frozen_checksum = self._checksum()
        self._protobuf.uuid = UUID(bytes=self._frozen_checksum).hex

    def _frozen(self) -> bool:
        uuid = self._protobuf.uuid
        self._protobuf.uuid = ''
        result = (self._checksum() == self._frozen_checksum) and (
            uuid == UUID(bytes=self._frozen_checksum).hex
        )
        self._protobuf.uuid = uuid
        return result

    def uuid(self) -> str:
        return self._protobuf.uuid

    def referring(
        self, type_name: t.Optional[str] = None
    ) -> t.Collection[st.Referring]:
        return self.storage().referring(self, type_name=type_name)

    def storage(self) -> storage_typing.Storage:
        return self._storage

    def set_remote(self, dataspec: st.DataSpec) -> None:
        """Add an Attribute to tag the DataSpec as remotely fetched."""
        attach_properties(
            dataspec,
            properties={
                # TODO deprecated in SDS >=2.0.0 -> remove property
                "is_remote": str(True)
            },
            name=IS_REMOTE,
        )

    def is_remote(self, dataspec: st.DataSpec) -> bool:
        """Is the dataspec a remotely defined dataset."""
        is_remote_att = self.attribute(IS_REMOTE, dataspec)
        return is_remote_att is not None

    def mock_value(
        self,
        transform: st.Transform,
        *arguments: st.DataSpec,
        **named_arguments: st.DataSpec,
    ) -> t.Any:
        """Compute the mock value of an external transform applied on
        Dataspecs.
        """
        raise NotImplementedError

    def infer_output_type(
        self,
        transform: st.Transform,
        *arguments: st.DataSpec,
        **named_arguments: st.DataSpec,
    ) -> t.Tuple[str, t.Callable[[st.DataSpec], None]]:
        """Infer the transform output type : minimal type inference."""

        def attach_nothing(ds: st.DataSpec) -> None:
            return

        # Some internal transforms return a Scalar
        if transform.spec() in [
            'protected_paths',
            'automatic_user_settings',
            'public_paths',
            'automatic_budget',
            'attribute_budget',
            'sd_budget',
            'sampling_ratios',
            'derive_seed',
            'relationship_spec',
        ]:
            return sp.type_name(sp.Scalar), attach_nothing

        # Other internal transforms return a Dataset
        if not transform.is_external():
            return sp.type_name(sp.Dataset), attach_nothing

        # Compute the mock value for external transforms
        mock_value = self.mock_value(transform, *arguments, **named_arguments)

        # Infer output types
        dataspec_type = (
            sp.type_name(sp.Dataset)
            if type(mock_value) in DATASET_TYPES
            else sp.type_name(sp.Scalar)
        )

        # Return the output type
        return dataspec_type, attach_nothing

    def schema(self, dataset: st.Dataset) -> st.Schema:
        raise NotImplementedError

    async def async_schema(self, dataset: st.Dataset) -> st.Schema:
        raise NotImplementedError

    def to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.Iterator[pa.RecordBatch]:
        raise NotImplementedError

    async def async_to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    def to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        raise NotImplementedError

    async def async_to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        raise NotImplementedError

    def to_parquet(self, dataset: st.Dataset) -> None:
        raise NotImplementedError

    async def async_to_parquet(self, dataset: st.Dataset) -> None:
        raise NotImplementedError

    def to_tensorflow(self, dataset: st.Dataset) -> tf.data.Dataset:
        raise NotImplementedError

    async def async_to_tensorflow(
        self, dataset: st.Dataset
    ) -> tf.data.Dataset:
        raise NotImplementedError

    def value(self, scalar: st.Scalar) -> st.DataSpecValue:
        raise NotImplementedError

    async def async_value(self, scalar: st.Scalar) -> st.DataSpecValue:
        raise NotImplementedError

    def cache_scalar(self, scalar: st.Scalar) -> None:
        raise NotImplementedError

    async def async_cache_scalar(self, scalar: st.Scalar) -> None:
        raise NotImplementedError

    def size(self, dataset: st.Dataset) -> st.Size:
        raise NotImplementedError

    async def async_size(self, dataset: st.Dataset) -> st.Size:
        raise NotImplementedError

    def bounds(self, dataset: st.Dataset) -> st.Bounds:
        raise NotImplementedError

    async def async_bounds(self, dataset: st.Dataset) -> st.Bounds:
        raise NotImplementedError

    def marginals(self, dataset: st.Dataset) -> st.Marginals:
        raise NotImplementedError

    async def async_marginals(self, dataset: st.Dataset) -> st.Marginals:
        raise NotImplementedError

    def status(
        self, dataspec: st.DataSpec, task_name: str
    ) -> t.Optional[st.Status]:
        return stt.last_status(
            dataspec=dataspec,
            manager=self,
            task=task_name,
        )

    def sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Mapping[t.Union[str, t.Tuple[str, ...]], str]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> t.Iterator[pa.RecordBatch]:
        raise NotImplementedError

    async def async_sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Mapping[t.Union[str, t.Tuple[str, ...]], str]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    def to_sql(self, dataset: st.Dataset) -> None:
        raise NotImplementedError

    async def async_to_sql(self, dataset: st.Dataset) -> None:
        raise NotImplementedError

    def foreign_keys(self, dataset: st.Dataset) -> t.Dict[st.Path, st.Path]:
        raise NotImplementedError

    def primary_keys(self, dataset: st.Dataset) -> t.List[st.Path]:
        raise NotImplementedError

    def is_big_data(self, dataset: st.Dataset) -> bool:
        status = self.status(dataset, task_name=BIG_DATA_TASK)

        if status is not None:
            # check if big_data_present
            big_data_task = status.task(BIG_DATA_TASK)
            # if yes:return answer
            if (big_data_task is not None) and (
                big_data_task.stage() == 'ready'
            ):
                return big_data_task.properties()[IS_BIG_DATA] == str(True)

        if dataset.is_source():
            raise NotImplementedError(
                'Found source dataset without any big data status'
            )
        else:
            if dataset.transform().is_external():
                return False
            parents_list, parents_dict = dataset.parents()
            ds_args = [
                element
                for element in parents_list
                if element.type_name() == sp.type_name(sp.Dataset)
            ]
            for element in parents_dict.values():
                if element.type_name() == sp.type_name(sp.Dataset):
                    ds_args.append(element)
            # parents_list.extend(list(parents_dict.values()))
            # parents_list=t.cast(t.Sequence[st.Dataset],parents_list)
            if len(ds_args) > 1:
                raise NotImplementedError(
                    'transforms with many dataspecs not supported yet'
                )
            is_parent_big_data = self.is_big_data(
                ds_args[0]  # type:ignore
            )

            if not is_parent_big_data:
                # write status it is not big data
                stt.ready(
                    dataset,
                    task=BIG_DATA_TASK,
                    properties={
                        IS_BIG_DATA: str(False)
                    },  # we do not need to add more info because a
                    # non big_data dataset cannot become big_data
                )
                return False
            else:
                # check that the transform does not change
                # the big data status
                (
                    is_big_data,
                    number_lines,
                    number_bytes,
                    threshold_kind,
                ) = check_transform_big_data(
                    dataset.transform(),
                    parents_list[0],  # type:ignore
                    parents_dict,
                )
                big_data_threshold = int(
                    stt.last_status(
                        dataspec=parents_list[0], task=BIG_DATA_TASK
                    )  # type:ignore
                    .task(BIG_DATA_TASK)
                    .properties()[BIG_DATA_THRESHOLD]
                )
                # write status
                stt.ready(
                    dataset,
                    task=BIG_DATA_TASK,
                    properties={
                        IS_BIG_DATA: str(is_big_data),
                        BIG_DATA_THRESHOLD: str(big_data_threshold),
                        DATASET_N_LINES: str(number_lines),
                        DATASET_N_BYTES: str(number_bytes),
                        THRESHOLD_TYPE: threshold_kind,
                    },
                )
                return is_big_data

    def is_cached(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def is_pushed_to_sql(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    async def async_primary_keys(self, dataset: st.Dataset) -> t.List[st.Path]:
        raise NotImplementedError

    async def async_foreign_keys(
        self, dataset: st.Dataset
    ) -> t.Dict[st.Path, st.Path]:
        raise NotImplementedError

    def attribute(
        self, name: str, dataspec: st.DataSpec
    ) -> t.Optional[st.Attribute]:
        attributes = t.cast(
            t.Set[st.Attribute],
            self.storage().referring(
                dataspec, type_name=sp.type_name(sp.Attribute)
            ),
        )
        filtered_attributes = [
            element for element in attributes if element.name() == name
        ]

        if len(filtered_attributes) == 0:
            return None

        if len(filtered_attributes) == 1:
            return t.cast(st.Attribute, filtered_attributes[0])

        raise ValueError('There are two attributes with the same name')

    def attributes(
        self, name: str, dataspec: st.DataSpec
    ) -> t.List[st.Attribute]:
        attributes = t.cast(
            t.Set[st.Attribute],
            self.storage().referring(
                dataspec, type_name=sp.type_name(sp.Attribute)
            ),
        )
        return [element for element in attributes if element.name() == name]

    def links(self, dataset: st.Dataset) -> st.Links:
        raise NotImplementedError

    def sql_pushing_schema_prefix(self, dataset: st.Dataset) -> str:
        raise NotImplementedError


def check_transform_big_data(
    transform: st.Transform,
    parent_dataset: st.Dataset,
    parents_dict: t.Mapping[str, st.DataSpec],
) -> t.Tuple[bool, int, int, str]:
    """This methods return true if the dataset transformed
    is big_data and False otherwise. This method is called when the parent
    is big_data so if the transform does not
    affect the size, it should return True
    """
    status = stt.last_status(parent_dataset, task=BIG_DATA_TASK)
    assert status
    big_data_threshold = int(
        status.task(BIG_DATA_TASK).properties()[  # type:ignore
            BIG_DATA_THRESHOLD
        ]
    )
    threshold_kind = status.task(BIG_DATA_TASK).properties()[  # type:ignore
        THRESHOLD_TYPE
    ]

    parent_n_lines_str = status.task(
        BIG_DATA_TASK
    ).properties()[  # type:ignore
        DATASET_N_LINES
    ]
    if parent_n_lines_str == '':
        parent_n_lines = 0
    else:
        parent_n_lines = int(parent_n_lines_str)

    parent_bytes_str = status.task(BIG_DATA_TASK).properties()[  # type:ignore
        DATASET_N_BYTES
    ]
    if parent_bytes_str == '':
        parent_bytes = 0
    else:
        parent_bytes = int(parent_bytes_str)

    transform_name = transform.name()
    if transform_name in ('Sample', 'DifferentiatedSample'):
        transform_type = transform.protobuf().spec.WhichOneof('spec')
        assert transform_type
        if getattr(transform.protobuf().spec, transform_type).HasField(
            'fraction'
        ):
            fraction = getattr(
                transform.protobuf().spec, transform_type
            ).fraction
            new_bytes = int(fraction * parent_bytes)
            n_lines = int(fraction * parent_n_lines)

            if threshold_kind == DATASET_N_BYTES:
                return (
                    new_bytes > big_data_threshold,
                    n_lines,
                    new_bytes,
                    threshold_kind,
                )
        else:
            n_lines = getattr(transform.protobuf().spec, transform_type).size
            new_bytes = int(n_lines * parent_bytes / parent_n_lines)

            if threshold_kind == DATASET_N_BYTES:
                big_data_threshold = int(1e5)

        threshold_kind = DATASET_N_LINES

        return n_lines > big_data_threshold, n_lines, new_bytes, threshold_kind

    elif transform_name == 'filter':
        # TODO: we need to save the real sizes of a dataspec in the statuses
        # so that we can check what happens here
        raise NotImplementedError(
            ' Big data status tot implemented yet for filtering'
        )

    elif transform_name == 'Synthetic data':
        # here we should leverage the sampling ratio just to get the size,
        # in any case, synthetic data is never big data
        sampling_ratios = t.cast(
            t.Mapping, t.cast(Scalar, parents_dict['sampling_ratios']).value()
        )
        synthetic_size = 0
        for table_path, sampling_ratio in zip(
            parent_dataset.schema().tables(), sampling_ratios.values()
        ):
            size = parent_dataset.size()
            assert size
            stat = size.statistics().nodes_statistics(table_path)[0]
            synthetic_size += int(stat.size() * sampling_ratio)
        threshold_kind = DATASET_N_LINES
        return (
            False,
            synthetic_size,
            int(synthetic_size * parent_bytes / parent_n_lines),
            threshold_kind,
        )
    elif transform_name == "select_sql":
        # TODO https://gitlab.com/sarus-tech/sarus-data-spec/-/issues/207
        return (False, -1, -1, threshold_kind)

    else:
        # other transforms do not affect size
        if transform_name == 'user_settings':
            warnings.warn(
                'user_settings transform considered to' 'not affect size'
            )
        return True, parent_n_lines, parent_bytes, threshold_kind
