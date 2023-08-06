import hashlib
import importlib
import inspect
import pickle as pkl
import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.schema import type_from_arrow_schema
from sarus_data_spec.config import ROUTING
from sarus_data_spec.dataspec_validator.typing import PEPKind
from sarus_data_spec.manager.async_utils import async_iter
from sarus_data_spec.manager.ops.asyncio.base import (
    DatasetImplementation,
    DatasetStaticChecker,
    DataspecStaticChecker,
    ScalarImplementation,
)
from sarus_data_spec.schema import schema as schema_builder
from sarus_data_spec.transform import external, transform_id
import sarus_data_spec.manager.typing as smt
import sarus_data_spec.protobuf as sp
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st

from .protection_utils import (
    ExternalOpImplementation,
    arguments_values,
    arguments_values_and_protected_entity,
    output_protected_entity,
    to_pyarrow_table_with_protected_entity,
)


class ExternalScalarStaticChecker(DataspecStaticChecker):
    async def private_queries(self) -> t.List[st.PrivateQuery]:
        """Return the PrivateQueries summarizing DP characteristics."""
        transform = self.dataspec.transform()
        ds_args, ds_kwargs = self.dataspec.parents()

        implementation = external_implementation(transform)
        args, kwargs = static_and_dynamic_arguments(
            transform, *ds_args, **ds_kwargs
        )
        return await implementation.private_queries(*args, **kwargs)

    def is_dp(self) -> bool:
        """Checks if the transform is DP and compatible with the arguments."""
        transform = self.dataspec.transform()
        ds_args, ds_kwargs = self.dataspec.parents()

        implementation = external_implementation(transform)
        args, kwargs = static_and_dynamic_arguments(
            transform, *ds_args, **ds_kwargs
        )
        return implementation.is_dp(*args, **kwargs)

    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PEP arguments are PEP and aligned
            (i.e. same PEP token)
            - other dataspecs arguments are public
        """
        transform = self.dataspec.transform()
        ds_args, ds_kwargs = self.dataspec.parents()

        implementation = external_implementation(transform)
        args, kwargs = static_and_dynamic_arguments(
            transform, *ds_args, **ds_kwargs
        )

        dp_implementation = implementation.dp_equivalent()
        if dp_implementation is None or not dp_implementation.is_dp(
            *args, **kwargs
        ):
            return False

        pep_args, non_pep_args = group_by_pep(
            dp_implementation, *args, **kwargs
        )

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return False

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in dp_implementation.allowed_pep_args:
            return False

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return False

        return True

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        transform = self.dataspec.transform()
        op_implementation = external_implementation(transform)
        py_args, py_kwargs, ds_args_pos = static_arguments(transform)

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return None

        dp_transform_id = dp_implementation.transform_id
        assert dp_transform_id is not None

        return external(
            dp_transform_id,
            py_args=py_args,
            py_kwargs=py_kwargs,
            ds_args_pos=ds_args_pos,
        )


class ExternalDatasetStaticChecker(
    ExternalScalarStaticChecker, DatasetStaticChecker
):
    def __init__(self, dataset: st.Dataset):
        super().__init__(dataset)
        self.dataset = dataset

    def pep_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """Return the current dataspec's PEP token."""
        transform = self.dataspec.transform()
        ds_args, ds_kwargs = self.dataspec.parents()

        implementation = external_implementation(transform)
        args, kwargs = static_and_dynamic_arguments(
            transform, *ds_args, **ds_kwargs
        )

        if len(implementation.allowed_pep_args) == 0:
            return None

        pep_args, non_pep_args = group_by_pep(implementation, *args, **kwargs)

        pep_kind = implementation.pep_kind(*args, **kwargs)
        if pep_kind == PEPKind.NOT_PEP:
            return None

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return None

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in implementation.allowed_pep_args:
            return None

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return None

        # The result is PEP, now check if it's aligned with the input(s)
        input_token = pep_tokens[0]
        assert input_token is not None
        if pep_kind == PEPKind.TOKEN_PRESERVING:
            output_token = input_token
        else:
            h = hashlib.md5()
            h.update(input_token.encode("ascii"))
            h.update(self.dataspec.transform().protobuf().SerializeToString())
            output_token = h.hexdigest()

        return output_token

    async def schema(self) -> st.Schema:
        """Computes the schema of the dataspec.

        The schema is computed by computing the synthetic data value and
        converting the Pyarrow schema to a Sarus schema.q
        """
        syn_variant = self.dataset.variant(kind=st.ConstraintKind.SYNTHETIC)
        assert syn_variant is not None
        assert syn_variant.prototype() == sp.Dataset

        syn_dataset = t.cast(st.Dataset, syn_variant)
        arrow_iterator = await syn_dataset.async_to_arrow(batch_size=1)
        first_batch = await arrow_iterator.__anext__()
        schema = first_batch.schema

        schema_type = type_from_arrow_schema(schema)
        if self.dataset.is_pep() and not schema_type.has_protected_format():
            # The synthetic schema might not have the protection, we need to
            # add it in this case
            schema_type = sdt.protected_type(schema_type)

        return schema_builder(self.dataset, schema_type=schema_type)


class ExternalDatasetOp(DatasetImplementation):
    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        transform = self.dataset.transform()
        ds_args, ds_kwargs = self.dataset.parents()

        implementation = external_implementation(transform)
        args, kwargs = static_and_dynamic_arguments(
            transform, *ds_args, **ds_kwargs
        )

        static_checker = ExternalDatasetStaticChecker(self.dataset)
        if static_checker.is_dp():
            (
                data_args,
                data_kwargs,
                pe,
            ) = await arguments_values_and_protected_entity(*args, **kwargs)
            result = await implementation.call(
                *data_args, **data_kwargs, pe=pe, dataspec=self.dataset
            )
            table = to_pyarrow_table(result)

        elif self.dataset.is_pep():
            (
                data_args,
                data_kwargs,
                pe,
            ) = await arguments_values_and_protected_entity(*args, **kwargs)
            result = await implementation.call(*data_args, **data_kwargs)
            output_pe = output_protected_entity(pe, result)
            table = to_pyarrow_table_with_protected_entity(result, output_pe)

        else:
            data_args, data_kwargs = await arguments_values(*args, **kwargs)
            result = await implementation.call(*data_args, **data_kwargs)
            table = to_pyarrow_table(result)

        return async_iter(table.to_batches(max_chunksize=batch_size))


class ExternalScalarOp(ScalarImplementation):
    async def value(self) -> t.Any:
        transform = self.scalar.transform()
        ds_args, ds_kwargs = self.scalar.parents()
        return await async_compute_external_value(
            transform, *ds_args, **ds_kwargs
        )


async def async_compute_external_value(
    transform: st.Transform,
    *ds_args: st.DataSpec,
    **ds_kwargs: st.DataSpec,
) -> t.Any:
    """Compute the value of an external transform applied on Dataspecs.

    This function computes the output value without manipulating the
    corresponding Dataspec. This is useful when we need to have access
    to the value of a Dataspec before its creation:
      - for computing a Mock value and inferring if the result is
        a Scalar or a Dataset.
    """
    implementation = external_implementation(transform)
    args, kwargs = static_and_dynamic_arguments(
        transform, *ds_args, **ds_kwargs
    )

    if implementation.is_dp(*args, **kwargs):
        data = await implementation.call(*args, **kwargs)

    else:
        data_args, data_kwargs = await arguments_values(*args, **kwargs)
        data = await implementation.call(*data_args, **data_kwargs)

    return data


def to_pyarrow_table(data: t.Any) -> pa.Table:
    """Convert the result of an external transform to a Pyarrow Table."""
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Cannot convert {type(data)} to Arrow batches.")

    df = t.cast(pd.DataFrame, data)
    return pa.Table.from_pandas(df)


def group_by_pep(
    op_implementation: smt.ExternalOpImplementation,
    *args: t.Any,
    **kwargs: t.Any,
) -> t.Tuple[t.Dict[str, st.DataSpec], t.Dict[str, st.DataSpec]]:
    """Get Dataspec arguments and split them between PEP and non PEP.

    This also identifies positional arguments by names based on the `call`
    signature.
    """
    # Add name to positional arguments to identify them by their names
    n_args = len(args)
    argument_names = list(
        inspect.signature(op_implementation.call).parameters.keys()
    )
    """
    Example :
    In [1]: def foo(a, b=3):
    ...:     return a+b
    ...:

    In [2]: list(inspect.signature(foo).parameters.keys())
    Out[2]: ['a', 'b']
    """
    for arg_name, arg_val in zip(argument_names[:n_args], args):
        # put all args in kwargs
        kwargs[arg_name] = arg_val

    # Keep only dataspec args and split PEP from non PEP
    dataspec_args = {
        arg_name: arg
        for arg_name, arg in kwargs.items()
        if isinstance(arg, st.DataSpec)
    }
    pep_args = {
        arg_name: arg
        for arg_name, arg in dataspec_args.items()
        if arg.is_pep()
    }
    non_pep_args = {
        arg_name: arg
        for arg_name, arg in dataspec_args.items()
        if arg_name not in pep_args
    }
    return pep_args, non_pep_args


def static_arguments(
    transform: st.Transform,
) -> t.Tuple[t.Dict[int, t.Any], t.Dict[str, t.Any], t.List[int]]:
    """Return the external arguments serialized in the protobuf."""
    assert transform and transform.is_external()

    transform_spec = transform.protobuf().spec
    external_args = pkl.loads(transform_spec.external.named_arguments)
    py_args = external_args["py_args"]
    py_kwargs = external_args["py_kwargs"]
    ds_args_pos = external_args["ds_args_pos"]
    return py_args, py_kwargs, ds_args_pos


def static_and_dynamic_arguments(
    transform: st.Transform, *ds_args: st.DataSpec, **ds_kwargs: st.DataSpec
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
    """Return all the external arguments.

    This returns static arguments interleaved with Dataspecs.
    """
    py_args, py_kwargs, ds_args_pos = static_arguments(transform)
    pos_values = {pos: val for pos, val in zip(ds_args_pos, ds_args)}
    kwargs = {**py_kwargs, **ds_kwargs}
    pos_args = {**pos_values, **py_args}
    args = [pos_args[i] for i in range(len(pos_args))]
    return args, kwargs


def external_implementation(
    transform: st.Transform,
) -> smt.ExternalOpImplementation:
    """Return the implementation of an external op from a DataSpec.

    The mapping is done by the config file.
    """
    assert transform and transform.is_external()
    library, op_name = transform_id(transform).split(".")
    if op_name not in ROUTING["external"][library]:
        raise NotImplementedError(
            f"Routing: {op_name} not in {list(ROUTING['external'][library].keys())}"  # noqa: E501
        )

    implementation_name = ROUTING["external"][library][op_name]
    module = importlib.import_module(
        f"sarus_data_spec.manager.ops.asyncio.processor.external.{library}"
    )
    op_implementation = getattr(module, implementation_name)

    if not isinstance(op_implementation, type):
        op_implementation = type(
            implementation_name,
            (ExternalOpImplementation,),
            {
                "call": staticmethod(op_implementation),
                "transform_id": transform_id,
            },
        )

    return t.cast(smt.ExternalOpImplementation, op_implementation())
