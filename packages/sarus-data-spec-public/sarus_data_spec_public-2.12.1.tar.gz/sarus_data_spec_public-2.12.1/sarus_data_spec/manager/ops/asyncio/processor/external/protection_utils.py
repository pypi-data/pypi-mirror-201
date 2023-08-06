from __future__ import annotations

import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.constants import DATA, PUBLIC, USER_COLUMN, WEIGHTS
from sarus_data_spec.dataspec_validator.typing import PEPKind
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class ExternalOpImplementation:
    """External PEP op implementation class.

    This class wraps together several elements of an external op
    implementation:
        - `call` is the function that computes the output value from the
          input(s) value(s).
    """

    transform_id: str
    _dp_equivalent: t.Optional[t.Type[ExternalOpImplementation]] = None
    allowed_pep_args: t.List[t.Set[str]] = []

    def dp_equivalent(self) -> t.Optional[ExternalOpImplementation]:
        if not self._dp_equivalent:
            return None
        return self._dp_equivalent()

    @staticmethod
    async def call(*args: t.Any, **kwargs: t.Any) -> t.Any:
        raise NotImplementedError

    def pep_kind(self, *args: t.Any, **kwargs: t.Any) -> PEPKind:
        """Return the PEP properties of the transform.

        It takes the transform arguments as input because it can depend on some
        transform parameters. For instance, it is not PEP if we are aggregating
        the rows (axis=0) and it is PEP if we are aggregating the columns
        (axis=1).

        NB: This function should have the same signature as the call function.
        """
        # Default implementation
        return PEPKind.NOT_PEP

    def is_dp(self, *args: t.Any, **kwargs: t.Any) -> bool:
        """Return True if the DP transform is compatible with the arguments.

        It takes the transform arguments as input because it can depend on some
        transform parameters. For instance, if we are aggregating the rows
        (axis=0), then there might be an equivalent DP transform but if we are
        aggregating the columns there might not (axis=1).

        NB: This function should have the same signature as the call function.
        """
        return False

    async def private_queries(
        self,
        *args: t.Any,
        budget: t.Optional[st.Scalar] = None,
        seed: t.Optional[st.Scalar] = None,
        **kwargs: t.Any,
    ) -> t.List[st.PrivateQuery]:
        """Takes as input the args of the transform (static and dynamic)."""
        if budget is None or seed is None:
            return []
        # Evaluate budget and seed
        budget_value = await budget.async_value()
        seed_value = await seed.async_value()
        queries, _ = await self.private_queries_and_task(
            *args, budget=budget_value, seed=seed_value, **kwargs
        )
        return queries

    @staticmethod
    async def private_queries_and_task(
        *args: t.Any, **kwargs: t.Any
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        raise NotImplementedError


async def arguments_values(
    *args: t.Any, **kwargs: t.Any
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
    """Evaluate sarus dataspecs among arguments.

    Compute the value of Dataspec arguments.
    """
    data_pe_args = [
        await eval_dataspec_and_exract_protected_entity(arg) for arg in args
    ]
    data_args = [data for data, _ in data_pe_args]

    data_pe_kwargs = {
        name: await eval_dataspec_and_exract_protected_entity(arg)
        for name, arg in kwargs.items()
    }
    data_kwargs = {name: data for name, (data, _) in data_pe_kwargs.items()}

    return data_args, data_kwargs


async def arguments_values_and_protected_entity(
    *args: t.Any, **kwargs: t.Any
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any], pd.DataFrame]:
    """Evaluate sarus dataspecs and extract the PE.

    Compute the value of Dataspec arguments. Extract all the protections,
    check that they are equal and return the PE value.
    """
    data_pe_args = [
        await eval_dataspec_and_exract_protected_entity(arg) for arg in args
    ]
    data_args = [data for data, _ in data_pe_args]
    pe_args = [pe for _, pe in data_pe_args]

    data_pe_kwargs = {
        name: await eval_dataspec_and_exract_protected_entity(arg)
        for name, arg in kwargs.items()
    }
    data_kwargs = {name: data for name, (data, _) in data_pe_kwargs.items()}
    pe_kwargs = [pe for _, pe in data_pe_kwargs.values()]

    input_protected_entities = list(
        filter(lambda x: x is not None, pe_args + pe_kwargs)
    )
    protected_entity = validate_protected_entity(input_protected_entities)

    return data_args, data_kwargs, protected_entity


def validate_protected_entity(
    protected_entities: t.List[pd.DataFrame],
) -> pd.DataFrame:
    """Check that all protected entities are equal."""
    # If we reach this part then there should be only one input PE
    pe = next(iter(protected_entities), None)
    if pe is None:
        raise ValueError("The dataset was infered PEP but has no input PE")
    # For now, PE in external ops are only viewed as pd.DataFrames
    if not all([candidate.equals(pe) for candidate in protected_entities]):
        raise ValueError(
            "The dataset is PEP but has several differing input PE values"
        )
    return pe


def output_protected_entity(
    input_pe: pd.DataFrame, output_value: pd.DataFrame
) -> pd.DataFrame:
    """Compute the output protected entity of an external transform."""
    # We guarantee that the data.index is a reliable way to trace how
    # the rows were rearranged
    return input_pe.loc[output_value.index]


async def eval_dataspec_and_exract_protected_entity(
    x: t.Union[t.Any, st.DataSpec]
) -> t.Tuple[t.Any, t.Optional[pd.DataFrame]]:
    """Compute the value of a DataSpec and extract its PE.

    Return None for the PE if it is not defined for the argument.
    """
    if not isinstance(x, st.DataSpec):
        return x, None
    if x.prototype() == sp.Dataset:
        dataset = t.cast(st.Dataset, x)
        df_with_pe = await dataset.async_to_pandas()
        return dataframe_split_data_and_protected_entity(df_with_pe)
    else:
        scalar = t.cast(st.Scalar, x)
        return await scalar.async_value(), None


def dataframe_split_data_and_protected_entity(
    raw_data: pd.DataFrame,
) -> t.Tuple[pd.DataFrame, t.Optional[pd.DataFrame]]:
    """Extract the protected entity from a pd.DataFrame.

    Return None for the PE is no PE is found on the DataFrame.
    """
    # TODO use `dataset.is_protected()` but we need the schema
    # for that, and it is not yet available in the SDK
    is_protected = set(raw_data.columns) == {
        PUBLIC,
        USER_COLUMN,
        WEIGHTS,
        DATA,
    }
    if is_protected:
        data = pd.DataFrame.from_records(
            raw_data[DATA].values, index=raw_data.index
        )
        pe = raw_data[[PUBLIC, USER_COLUMN, WEIGHTS]]
    else:
        data = raw_data
        pe = None
    return data, pe


def to_pyarrow_table_with_protected_entity(
    data: pd.DataFrame, pe: t.Optional[pd.DataFrame]
) -> pa.Table:
    """Merge a protection and its data in pandas.

    NB: we return directly the pa.Table otherwise the data column order is lost
    when doing pa.Table.from_pandas(df).to_pandas(). Another solution to
    preserve the column order would be to also return the Table schema and pass
    it as argument to pa.Table.from_pandas(df, schema)
    """
    if pe is not None:
        # Work with Arrow to preserve column order (vs Python dict)
        pe_table = pa.Table.from_pandas(pe)
        data_table = pa.Table.from_pandas(data)
        data_arrays = [
            chunked_array.combine_chunks()
            for chunked_array in data_table.columns
        ]
        data_array = pa.StructArray.from_arrays(
            data_arrays, names=data_table.column_names
        )
        result = pe_table.append_column(DATA, data_array)
    else:
        # TODO also wrap the data in an empty protection
        result = pa.Table.from_pandas(data)
    return result
