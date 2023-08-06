from typing import Any, List, Tuple, Union
import typing as t

import numpy as np
import pandas as pd
import pandas._typing as pdt

from sarus_data_spec.dataspec_validator.typing import PEPKind
import sarus_data_spec.typing as st

from ..protection_utils import ExternalOpImplementation
from .pandas_dp import (
    pd_mean_dp,
    pd_median_dp,
    pd_shape_dp,
    pd_std_dp,
    pd_sum_dp,
)

# Defined in pandas version > 1.3.5
IgnoreRaise = t.Literal["ignore", "raise"]


class pd_loc(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        key: Tuple[Union[str, slice, List[str]], ...],
    ) -> pd.DataFrame:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.loc[key]

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        key: Tuple[Union[str, slice, List[str]], ...],
    ) -> PEPKind:
        return PEPKind.PEP


class pd_iloc(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        key: Tuple[Union[str, slice, List[str]], ...],
    ) -> pd.DataFrame:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.iloc[key]

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        key: Tuple[Union[str, slice, List[str]], ...],
    ) -> PEPKind:
        return PEPKind.PEP


class pd_head(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        n: int = 5,
    ) -> Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.head(n=n)

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        n: int = 5,
    ) -> PEPKind:
        return PEPKind.PEP


class pd_astype(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        dtype: pdt.Dtype,
        copy: bool = True,
        errors: IgnoreRaise = "raise",
    ) -> pd.DataFrame:
        return parent_df.astype(dtype=dtype, copy=copy, errors=errors)

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        dtype: pdt.Dtype,
        copy: bool = True,
        errors: IgnoreRaise = "raise",
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_getitem(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame], key: t.Any
    ) -> t.Any:
        return parent_df[key]

    def pep_kind(  # type: ignore[override]
        self, parent_df: t.Union[pd.Series, pd.DataFrame], key: t.Any
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_shape(ExternalOpImplementation):
    _dp_equivalent = pd_shape_dp

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame]
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.shape


class pd_sum(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]
    _dp_equivalent = pd_sum_dp

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        axis: t.Optional[pdt.Axis] = None,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        min_count: int = 0,
    ) -> Any:
        assert type(parent_df) in [pd.DataFrame, pd.Series]
        return parent_df.sum(
            axis=axis,
            level=level,
            skipna=skipna,
            numeric_only=numeric_only,
            min_count=min_count,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        axis: t.Optional[pdt.Axis] = None,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING if axis == 1 else PEPKind.NOT_PEP


class pd_mean(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]
    _dp_equivalent = pd_mean_dp

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        axis: int = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: bool = False,
    ) -> Any:
        assert type(parent_df) in [pd.DataFrame, pd.Series]
        return parent_df.mean(
            axis=axis,
            skipna=skipna,
            level=level,
            numeric_only=numeric_only,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        axis: int = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: bool = False,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING if axis == 1 else PEPKind.NOT_PEP


class pd_std(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]
    _dp_equivalent = pd_std_dp

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        axis: int = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        ddof: int = 1,
        numeric_only: bool = False,
    ) -> t.Any:
        assert type(parent_df) in [pd.DataFrame, pd.Series]
        return parent_df.std(
            axis=axis,
            skipna=skipna,
            level=level,
            ddof=ddof,
            numeric_only=numeric_only,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: t.Any,
        axis: int = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        ddof: int = 1,
        numeric_only: bool = False,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING if axis == 1 else PEPKind.NOT_PEP


class pd_median(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]
    _dp_equivalent = pd_median_dp

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        axis: int = 0,
        skipna: bool = True,
        level: t.Optional[int] = None,
        numeric_only: bool = False,
    ) -> t.Any:
        assert type(parent_df) in [pd.DataFrame, pd.Series]
        return parent_df.median(
            axis=axis,
            skipna=skipna,
            level=level,
            numeric_only=numeric_only,
        )

    def pep_kind(  # type: ignore[override]
        self,
        dataframe: Any,
        axis: int = 0,
        skipna: bool = True,
        level: t.Optional[int] = None,
        numeric_only: bool = False,
        **kwargs: Any,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING if axis == 1 else PEPKind.NOT_PEP


class pd_abs(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame]
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.abs()

    def pep_kind(  # type: ignore[override]
        self, parent_df: st.DataSpec
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_drop(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Any,
        labels: pdt.IndexLabel = None,
        axis: pdt.Axis = 0,
        index: pdt.IndexLabel = None,
        columns: pdt.IndexLabel = None,
        level: pdt.Level = None,
        inplace: bool = False,
        errors: IgnoreRaise = "raise",
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.drop(
            axis=axis,
            labels=labels,
            index=index,
            columns=columns,
            level=level,
            inplace=False,  # need to be False or returns None
            errors=errors,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: t.Any,
        labels: pdt.IndexLabel = None,
        axis: pdt.Axis = 0,
        index: pdt.IndexLabel = None,
        columns: pdt.IndexLabel = None,
        level: pdt.Level = None,
        inplace: bool = False,
        errors: IgnoreRaise = "raise",
    ) -> PEPKind:
        if axis in [0, 'columns']:
            return PEPKind.PEP
        else:
            return PEPKind.TOKEN_PRESERVING


class pd_dropna(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Any,
        axis: pdt.Axis = 0,
        how: t.Optional[str] = None,
        thresh: t.Optional[int] = None,
        subset: pdt.IndexLabel = None,
        inplace: bool = False,
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.dropna(
            axis=axis, how=how, thresh=thresh, subset=subset, inplace=inplace
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: t.Any,
        axis: pdt.Axis = 0,
        how: t.Optional[str] = None,
        thresh: t.Optional[int] = None,
        subset: pdt.IndexLabel = None,
        inplace: bool = False,
    ) -> PEPKind:
        if axis in [0, 'columns']:
            return PEPKind.PEP
        else:
            return PEPKind.TOKEN_PRESERVING


class pd_fillna(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        value: t.Optional[
            t.Union[t.Hashable, t.Mapping, pd.Series, pd.DataFrame]
        ] = None,
        method: t.Optional[pdt.FillnaOptions] = None,
        axis: t.Optional[pdt.Axis] = None,
        inplace: bool = False,
        limit: t.Optional[int] = None,
        downcast: t.Optional[dict] = None,
    ) -> Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.fillna(
            value=value,
            method=method,
            axis=axis,
            inplace=False,  # need to be False or returns None
            limit=limit,
            downcast=downcast,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.Dataset,
        value: t.Optional[
            t.Union[t.Hashable, t.Mapping, pd.Series, pd.DataFrame]
        ] = None,
        method: t.Optional[pdt.FillnaOptions] = None,
        axis: t.Optional[pdt.Axis] = None,
        inplace: bool = False,
        limit: t.Optional[int] = None,
        downcast: t.Optional[dict] = None,
    ) -> PEPKind:
        if method is None:
            return PEPKind.TOKEN_PRESERVING
        else:
            return PEPKind.NOT_PEP


class pd_isin(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        values: t.Union[pd.Series, pd.DataFrame, pdt.Sequence, t.Mapping],
    ) -> t.Any:
        return parent_df.isin(values=values)

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.Dataset,
        values: t.Union[pd.Series, pd.DataFrame, pdt.Sequence, t.Mapping],
    ) -> t.Any:
        return PEPKind.TOKEN_PRESERVING


class pd_isnull(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame]
    ) -> Any:
        return parent_df.isnull()

    def pep_kind(  # type: ignore[override]
        self, parent_df: st.Dataset
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_mask(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        cond: t.Union[pd.Series, pd.DataFrame, t.Callable],
        other: t.Union[
            pdt.Scalar, pd.Series, pd.DataFrame, t.Callable
        ] = np.nan,
        inplace: bool = False,
        axis: t.Optional[pdt.Axis] = None,
        level: pdt.Level = None,
        errors: IgnoreRaise = "raise",
        try_cast: bool = False,
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.mask(
            cond=cond,
            other=other,
            inplace=False,  # need to be False or returns None
            axis=axis,
            level=level,
            errors=errors,
            try_cast=try_cast,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.Dataset,
        cond: t.Union[pd.Series, pd.DataFrame, t.Callable],
        other: t.Union[
            pdt.Scalar, pd.Series, pd.DataFrame, t.Callable
        ] = np.nan,
        inplace: bool = False,
        axis: t.Optional[pdt.Axis] = None,
        level: pdt.Level = None,
        errors: IgnoreRaise = "raise",
        try_cast: bool = False,
    ) -> PEPKind:
        if callable(cond) or callable(other):
            return PEPKind.NOT_PEP
        else:
            return PEPKind.TOKEN_PRESERVING


class pd_notnull(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame]
    ) -> Any:
        return parent_df.notnull()

    def pep_kind(  # type: ignore[override]
        self, parent_df: st.Dataset
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_rename(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        mapper: t.Optional[pdt.Renamer] = None,
        index: t.Optional[pdt.Renamer] = None,
        columns: t.Optional[pdt.Renamer] = None,
        axis: t.Optional[pdt.Axis] = None,
        copy: t.Optional[bool] = None,
        inplace: bool = False,
        level: pdt.Level = None,
        errors: IgnoreRaise = "ignore",
    ) -> Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.rename(
            mapper=mapper,
            index=index,
            columns=columns,
            axis=axis,
            copy=copy,
            inplace=False,  # need to be False or returns None
            level=level,
            errors=errors,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.Dataset,
        mapper: t.Optional[pdt.Renamer] = None,
        index: t.Optional[pdt.Renamer] = None,
        columns: t.Optional[pdt.Renamer] = None,
        axis: t.Optional[pdt.Axis] = None,
        copy: t.Optional[bool] = None,
        inplace: bool = False,
        level: pdt.Level = None,
        errors: IgnoreRaise = "ignore",
    ) -> PEPKind:
        if callable(mapper) or callable(index) or callable(columns):
            return PEPKind.NOT_PEP
        else:
            return PEPKind.TOKEN_PRESERVING


class pd_replace(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        to_replace: t.Union[
            str, t.List, t.Dict, pd.Series, int, float, None
        ] = None,
        value: t.Optional[t.Union[pdt.Scalar, t.Dict, t.List, str]] = None,
        inplace: bool = False,
        limit: t.Optional[int] = None,
        regex: bool = False,
        method: t.Optional[t.Literal["pad", "ffill", "bfill"]] = None,
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.replace(
            to_replace=to_replace,
            value=value,
            inplace=False,  # need to be False or returns None
            limit=limit,
            regex=regex,
            method=method,
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: t.Union[pd.Series, pd.DataFrame],
        to_replace: t.Union[
            str, t.List, t.Dict, pd.Series, int, float, None
        ] = None,
        value: t.Optional[t.Union[pdt.Scalar, t.Dict, t.List, str]] = None,
        inplace: bool = False,
        limit: t.Optional[int] = None,
        regex: bool = False,
        method: t.Optional[t.Literal["pad", "ffill", "bfill"]] = None,
    ) -> PEPKind:
        if value is None:
            return PEPKind.NOT_PEP
        else:
            return PEPKind.TOKEN_PRESERVING


class pd_round(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        decimals: t.Union[int, t.Dict[pdt.IndexLabel, int], pd.Series] = 0,
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.round(decimals=decimals)

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.Dataset,
        decimals: t.Union[int, t.Dict[pdt.IndexLabel, int], pd.Series] = 0,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_select_dtypes(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        include: t.Optional[t.Union[pdt.Scalar, t.List]] = None,
        exclude: t.Optional[t.Union[pdt.Scalar, t.List]] = None,
    ) -> t.Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.select_dtypes(include=include, exclude=exclude)

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        include: t.Optional[t.Union[pdt.Scalar, t.List]] = None,
        exclude: t.Optional[t.Union[pdt.Scalar, t.List]] = None,
    ) -> PEPKind:
        return PEPKind.PEP


class pd_add(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        other: t.Union[
            pdt.Scalar, t.Sequence, pd.Series, t.Dict, pd.DataFrame
        ],
        axis: pdt.Axis = 'columns',
        level: t.Optional[pdt.Level] = None,
        fill_value: t.Optional[float] = None,
    ) -> Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.add(
            other=other, axis=axis, level=level, fill_value=fill_value
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        other: t.Union[
            pdt.Scalar, t.Sequence, pd.Series, t.Dict, pd.DataFrame
        ],
        axis: pdt.Axis = 'columns',
        level: t.Optional[pdt.Level] = None,
        fill_value: t.Optional[float] = None,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


class pd_sub(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_df"}]

    @staticmethod
    async def call(  # type: ignore[override]
        parent_df: t.Union[pd.Series, pd.DataFrame],
        other: t.Union[
            pdt.Scalar, t.Sequence, pd.Series, t.Dict, pd.DataFrame
        ],
        axis: pdt.Axis = 'columns',
        level: t.Optional[pdt.Level] = None,
        fill_value: t.Optional[float] = None,
    ) -> Any:
        assert type(parent_df) in [pd.Series, pd.DataFrame]
        return parent_df.sub(
            other=other, axis=axis, level=level, fill_value=fill_value
        )

    def pep_kind(  # type: ignore[override]
        self,
        parent_df: st.DataSpec,
        other: t.Union[
            pdt.Scalar, t.Sequence, pd.Series, t.Dict, pd.DataFrame
        ],
        axis: pdt.Axis = 'columns',
        level: t.Optional[pdt.Level] = None,
        fill_value: t.Optional[float] = None,
    ) -> PEPKind:
        return PEPKind.TOKEN_PRESERVING


async def pd_sum_groupby(groupby: t.Any, *args: t.Any, **kwargs: t.Any) -> Any:
    """SUM operation specific for groupby objects."""
    assert isinstance(groupby, pd.core.groupby.GroupBy)
    return groupby.sum(*args, **kwargs)


async def pd_std_groupby(groupby: t.Any, *args: t.Any, **kwargs: t.Any) -> Any:
    """STD operation specific for groupby objects."""
    assert isinstance(groupby, pd.core.groupby.GroupBy)
    return groupby.std(*args, **kwargs)


async def pd_mean_groupby(
    groupby: t.Any, *args: t.Any, **kwargs: t.Any
) -> Any:
    """MEAN operation specific for groupby objects."""
    assert isinstance(groupby, pd.core.groupby.GroupBy)
    return groupby.mean(*args, **kwargs)


async def pd_median_groupby(
    groupby: t.Any, *args: t.Any, **kwargs: t.Any
) -> Any:
    """MEDIAN operation specific for groupby objects."""
    assert isinstance(groupby, pd.core.groupby.GroupBy)
    return groupby.median(*args, **kwargs)


async def pd_ndim(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.ndim


async def pd_dataframe(*args: Any, **kwargs: Any) -> Any:
    return pd.DataFrame(*args, **kwargs)


async def pd_series(*args: Any, **kwargs: Any) -> Any:
    return pd.Series(*args, **kwargs)


async def pd_query(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.DataFrame]
    return parent_val.query(*args, **kwargs)


async def pd_groups(parent_val: Any) -> Any:
    return parent_val.groups


async def pd_name(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.name


async def pd_size(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.size


async def pd_axes(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.axes


async def pd_columns(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.columns


async def pd_index(parent_val: Any) -> pd.DataFrame:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.index


async def pd_dtype(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.dtype


async def pd_dtypes(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.dtypes


async def pd_values(parent_val: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.values


async def pd_reset_index(
    parent_val: Any, *args: Any, **kwargs: Any
) -> pd.DataFrame:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.reset_index(*args, **kwargs)


async def pd_set_loc(
    parent_val: Any,
    key: Tuple[Union[str, slice, List[str]], ...],
    newvalue: Any,
) -> pd.DataFrame:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    parent_val.loc[key] = newvalue
    return parent_val


async def pd_set_iloc(
    parent_val: Any,
    key: Tuple[Union[str, slice, List[str]], ...],
    newvalue: Any,
) -> pd.DataFrame:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    parent_val.iloc[key] = newvalue
    return parent_val


async def pd_eq(val_1: Any, val_2: Any) -> pd.DataFrame:
    return val_1 == val_2


async def pd_min(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.min(*args, **kwargs)


async def pd_max(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.max(*args, **kwargs)


async def pd_shift(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.shift(*args, **kwargs)


async def pd_any(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.any(*args, **kwargs)


async def pd_describe(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.describe(*args, **kwargs)


async def pd_quantile(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.quantile(*args, **kwargs)


async def pd_reindex(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.reindex(*args, **kwargs)


async def pd_count(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.count(*args, **kwargs)


async def pd_transpose(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.transpose(*args, **kwargs)


async def pd_unique(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.unique(*args, **kwargs)


async def pd_value_counts(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.value_counts(*args, **kwargs)


async def pd_to_dict(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.to_dict(*args, **kwargs)


async def pd_apply(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.apply(*args, **kwargs)


async def pd_mad(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.mad(*args, **kwargs)


async def pd_skew(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.skew(*args, **kwargs)


async def pd_kurtosis(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.kurtosis(*args, **kwargs)


async def pd_agg(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.agg(*args, **kwargs)


async def pd_droplevel(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.droplevel(*args, **kwargs)


async def pd_sort_values(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.sort_values(*args, **kwargs)


async def pd_drop_duplicates(
    parent_val: Any, *args: Any, **kwargs: Any
) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.drop_duplicates(*args, **kwargs)


async def pd_corr(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return parent_val.corr(*args, **kwargs)


async def pd_get_dummies(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    assert type(parent_val) in [pd.Series, pd.DataFrame]
    return pd.get_dummies(parent_val, *args, **kwargs)


async def pd_join(val1: Any, *args: Any, **kwargs: Any) -> Any:
    return val1.join(*args, **kwargs)


async def pd_groupby(val1: Any, *args: Any, **kwargs: Any) -> Any:
    return val1.groupby(*args, **kwargs)


async def pd_merge(val1: Any, *args: Any, **kwargs: Any) -> Any:
    return val1.merge(*args, **kwargs)


async def pd_merge_fn(*args: Any, **kwargs: Any) -> Any:
    return pd.merge(*args, **kwargs)


async def pd_concat(*args: Any, **kwargs: Any) -> Any:
    return pd.concat(*args, **kwargs)


async def pd_append(val1: Any, *args: Any, **kwargs: Any) -> Any:
    return val1.append(*args, **kwargs)


async def pd_nunique(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.nunique(*args, **kwargs)


async def pd_rolling(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.rolling(*args, **kwargs)


async def pd_union(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.union(*args, **kwargs)


async def pd_to_datetime(*args: Any, **kwargs: Any) -> Any:
    return pd.to_datetime(*args, **kwargs)
