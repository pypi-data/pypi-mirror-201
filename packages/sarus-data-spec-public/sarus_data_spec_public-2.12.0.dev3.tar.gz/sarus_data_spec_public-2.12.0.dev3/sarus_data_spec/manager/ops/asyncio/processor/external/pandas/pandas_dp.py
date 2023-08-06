import logging
import typing as t

import numpy as np
import pandas as pd
import pandas._typing as pdt

from sarus_data_spec.constants import MAX_MAX_MULT
from sarus_data_spec.protobuf.utilities import unwrap
import sarus_data_spec.typing as st

from ..protection_utils import (
    ExternalOpImplementation,
    arguments_values,
    arguments_values_and_protected_entity,
)

logger = logging.getLogger(__name__)

try:
    from sarus_statistics.ops.bounds.op import BoundOp
    from sarus_statistics.ops.histograms.op import CountOp
    from sarus_statistics.ops.max_multiplicity.op import MaxMultiplicityOp
    from sarus_statistics.ops.mean.op import MeanOp
    from sarus_statistics.ops.median.op import MedianOp
    from sarus_statistics.ops.std.op import StdOp
    from sarus_statistics.ops.sum.op import SumOp
    from sarus_statistics.protobuf.size_pb2 import MaxMultiplicity
except ModuleNotFoundError:
    pass  # warning raised in typing

try:
    from sarus_differential_privacy.query import ComposedPrivateQuery
except ModuleNotFoundError:
    pass  # warning raised in typing

try:
    from sarus_query_builder.builders.bounds_builder import (
        simple_bounds_builder,
    )
    from sarus_query_builder.builders.composed_builder import (
        simple_composed_builder,
    )
    from sarus_query_builder.builders.max_multiplicity_builder import (
        simple_max_multiplicity_builder,
    )
    from sarus_query_builder.builders.mean_builder import mean_builder
    from sarus_query_builder.builders.median_builder import median_builder
    from sarus_query_builder.builders.standard_mechanisms_builder import (
        laplace_builder,
    )
    from sarus_query_builder.builders.std_builder import std_builder
    from sarus_query_builder.builders.sum_builder import sum_builder
    from sarus_query_builder.core.core import OptimizableQueryBuilder
    from sarus_query_builder.protobuf.query_pb2 import GenericTask, Query
except ModuleNotFoundError:
    pass  # warning raised in typing


DEFAULT_MAX_MAX_MULT = 1
NUMERIC_TYPES = ('integer', 'float', 'boolean')


class pd_shape_dp(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_ds"}]
    transform_id: str = "pandas.PD_SHAPE_DP"

    def is_dp(self, *args: t.Any, **kwargs: t.Any) -> bool:
        return True

    @staticmethod
    async def private_queries_and_task(  # type: ignore[override]
        parent_ds: st.Dataset, budget: t.Any, **kwargs: t.Any
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        """Return the PrivateQueries summarizing DP characteristics."""
        if len(budget) != 1:
            raise NotImplementedError(
                "The PrivacyParams contains more than 1 point in the privacy "
                "profile."
            )

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )

        epsilon = budget[0].epsilon
        delta = budget[0].delta
        if epsilon == 0.0:
            raise ValueError("`epsilon` should be greater than 0.")

        builder = simple_composed_builder(
            parent_ds,
            [
                simple_max_multiplicity_builder(
                    parent_ds,
                    Query(
                        max_multiplicity=Query.MaxMultiplicity(
                            max_max_multiplicity=max_max_mult
                        )
                    ),
                ),
                laplace_builder(
                    parent_ds,
                    Query(laplace_mechanism=Query.LaplaceMechanism()),
                ),
            ],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    @staticmethod
    async def call(  # type: ignore[override]
        parent_ds: st.Dataset,
        budget: st.Scalar,
        seed: st.Scalar,
    ) -> t.Any:
        """Implementation of DP shape.

        A DP implementation receives additional arguments compared to a
        standard external implementation:
            - `budget`: a list of sp.Scalar.PrivacyParams.Point
                object containing each an epsilon and a delta values
            - `seed`: an integer used to parametrize random number generators
            - `pe`: theprotected entity used by `sarus_statistics` primitives
        """
        # Evaluate arguments
        (dataframe, budget_value, seed_value), _ = await arguments_values(
            parent_ds, budget, seed
        )

        # Get QB task parametrization
        _, tasks = await pd_shape_dp.private_queries_and_task(
            parent_ds, budget_value
        )

        epsilon = budget_value[0].epsilon
        n_rows, n_cols = dataframe.shape

        # Compute DP value
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, shape_task = t.cast(MaxMultiplicity, tasks[0]), t.cast(
            GenericTask, tasks[1]
        )
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        n_rows = CountOp(
            parent_ds,
            noise=shape_task.parameters['noise'],
        ).value(max_mul, random_generator)

        dp_shape = (n_rows, n_cols)

        # Compute private query
        return dp_shape


class pd_sum_dp(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_ds"}]
    transform_id: str = "pandas.PD_SUM_DP"

    def is_dp(  # type: ignore[override]
        self,
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = None,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        min_count: int = 0,
        budget: t.Any = None,
        seed: t.Optional[int] = None,
        **kwargs: t.Any,
    ) -> bool:
        return (axis == 0) and (numeric_only is True)

    @staticmethod
    async def private_queries_and_task(  # type: ignore[override]
        parent_ds: st.Dataset,
        budget: t.Any,
        **kwargs: t.Any,
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        if len(budget) != 1:
            raise NotImplementedError(
                "The PrivacyParams contains more than 1 point in the privacy "
                "profile."
            )

        epsilon = budget[0].epsilon
        delta = budget[0].delta
        if epsilon == 0.0:
            raise ValueError("`epsilon` should be greater than 0.")

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )

        column_bounds_sum_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    sum_builder(parent_ds, Query(sum=Query.Sum())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_sum_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    @staticmethod
    async def call(  # type: ignore[override]
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = None,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        min_count: int = 0,
        budget: t.Optional[st.Scalar] = None,
        seed: t.Optional[st.Scalar] = None,
        **kwargs: t.Any,
    ) -> t.Any:
        # Evaluate arguments
        (dataframe, budget_value, seed_value), _ = await arguments_values(
            parent_ds, budget, seed
        )

        assert type(dataframe) in [pd.DataFrame, pd.Series]
        assert numeric_only
        assert axis == 0
        assert level is None
        assert min_count == 0
        assert seed_value
        assert budget_value

        _, tasks = await pd_sum_dp.private_queries_and_task(
            parent_ds=parent_ds,
            budget=budget_value,
        )

        epsilon = budget_value[0].epsilon
        # Compute DP value
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, sum_tasks = tasks[0], tasks[1:]
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        sum_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            subtasks = [unwrap(task) for task in sum_tasks[index].subtasks]
            bounds_parameters, sum_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    sum_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            # TODO parent_ds doesn't have a size
            # if parent_ds.size().children()[column_name].size() < min_count:
            #     sum_dp_dict[column_name] = np.nan
            #     continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            sum_op = SumOp(
                parent_ds,
                sum_parameters.parameters['noise'],
            )
            sum_dp_dict[column_name] = sum_op.value(
                column_name, max_mul, bounds, random_generator
            )

        sum_dp = pd.Series(sum_dp_dict)
        return sum_dp


class pd_mean_dp(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_ds"}]
    transform_id: str = "pandas.PD_MEAN_DP"

    def is_dp(  # type: ignore[override]
        self,
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        budget: t.Any = None,
        seed: t.Optional[int] = None,
        **kwargs: t.Any,
    ) -> bool:
        return axis == 0 and numeric_only is True

    @staticmethod
    async def private_queries_and_task(  # type: ignore[override]
        parent_ds: st.Dataset,
        budget: t.Any,
        **kwargs: t.Any,
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        if len(budget) != 1:
            raise NotImplementedError(
                "The PrivacyParams contains more than 1 point in the privacy "
                "profile."
            )

        epsilon = budget[0].epsilon
        delta = budget[0].delta
        if epsilon == 0.0:
            raise ValueError("`epsilon` should be greater than 0.")

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_bounds_mean_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    mean_builder(parent_ds, Query(mean=Query.Mean())),
                ],
            )
        )
        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_mean_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    @staticmethod
    async def call(  # type: ignore[override]
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        budget: t.Optional[st.Scalar] = None,
        seed: t.Optional[st.Scalar] = None,
        **kwargs: t.Any,
    ) -> t.Any:
        # Evaluate arguments
        (
            (dataframe, budget_value, seed_value),
            _,
            pe,
        ) = await arguments_values_and_protected_entity(
            parent_ds, budget, seed
        )

        assert type(dataframe) in [pd.DataFrame, pd.Series]
        assert pe.shape[0] == dataframe.shape[0]
        assert numeric_only
        assert axis == 0
        assert level is None
        assert seed_value
        assert budget_value

        _, tasks = await pd_mean_dp.private_queries_and_task(
            parent_ds=parent_ds,
            budget=budget_value,
        )
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, mean_tasks = tasks[0], tasks[1:]

        # Compute DP value
        random_generator = np.random.default_rng(abs(seed_value))
        epsilon = budget_value[0].epsilon
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        mean_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            df = dataframe[[column_name]].join(pe)
            subtasks = [unwrap(task) for task in mean_tasks[index].subtasks]
            bounds_parameters, mean_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    mean_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
                df = df.dropna()
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            mean_op = MeanOp(
                parent_ds,
                mean_parameters.parameters['noise'],
            )
            mean_dp_dict[column_name] = mean_op.value(
                column_name, max_mul, bounds, random_generator
            )

        mean_dp = pd.Series(mean_dp_dict)
        return mean_dp


class pd_median_dp(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_ds"}]
    transform_id: str = "pandas.PD_MEDIAN_DP"

    def is_dp(  # type: ignore[override]
        self,
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        budget: t.Any = None,
        seed: t.Optional[int] = None,
        **kwargs: t.Any,
    ) -> bool:
        return axis == 0 and numeric_only is True

    @staticmethod
    async def private_queries_and_task(  # type: ignore[override]
        parent_ds: st.Dataset,
        budget: t.Any,
        **kwargs: t.Any,
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        if len(budget) != 1:
            raise NotImplementedError(
                "The PrivacyParams contains more than 1 point in the privacy "
                "profile."
            )

        epsilon = budget[0].epsilon
        delta = budget[0].delta
        if epsilon == 0.0:
            raise ValueError("`epsilon` should be greater than 0.")

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_bounds_median_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    median_builder(parent_ds, Query(median=Query.Median())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_median_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    @staticmethod
    async def call(  # type: ignore[override]
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        budget: t.Optional[st.Scalar] = None,
        seed: t.Optional[st.Scalar] = None,
        **kwargs: t.Any,
    ) -> t.Any:
        # Evaluate arguments
        (
            (dataframe, budget_value, seed_value),
            _,
            pe,
        ) = await arguments_values_and_protected_entity(
            parent_ds, budget, seed
        )

        assert type(dataframe) in [pd.DataFrame, pd.Series]
        assert pe.shape[0] == dataframe.shape[0]
        assert numeric_only
        assert axis == 0
        assert level is None
        assert seed_value
        assert budget_value

        _, tasks = await pd_median_dp.private_queries_and_task(
            parent_ds=parent_ds,
            budget=budget_value,
        )
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, median_tasks = tasks[0], tasks[1:]

        random_generator = np.random.default_rng(abs(seed_value))
        epsilon = budget_value[0].epsilon

        # Compute DP value
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        median_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            df = dataframe[[column_name]].join(pe)
            subtasks = [unwrap(task) for task in median_tasks[index].subtasks]
            bounds_parameters, median_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    median_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
                df = df.dropna()
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            median_op = MedianOp(
                parent_ds,
                median_parameters.parameters['noise'],
            )
            median_dp_dict[column_name] = median_op.value(
                column_name, max_mul, bounds, random_generator
            )

        median_dp = pd.Series(median_dp_dict)
        return median_dp


class pd_std_dp(ExternalOpImplementation):
    allowed_pep_args: t.List[t.Set[str]] = [{"parent_ds"}]
    transform_id: str = "pandas.PD_STD_DP"

    def is_dp(  # type: ignore[override]
        self,
        parent_ds: t.Any,
        axis: t.Optional[pdt.Axis] = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        ddof: int = 1,
        budget: t.Any = None,
        seed: t.Optional[int] = None,
        **kwargs: t.Any,
    ) -> bool:
        return axis == 0 and numeric_only is True

    @staticmethod
    async def private_queries_and_task(  # type: ignore[override]
        parent_ds: st.Dataset,
        budget: t.Any,
        **kwargs: t.Any,
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        if len(budget) != 1:
            raise NotImplementedError(
                "The PrivacyParams contains more than 1 point in the privacy "
                "profile."
            )

        epsilon = budget[0].epsilon
        delta = budget[0].delta
        if epsilon == 0.0:
            raise ValueError("`epsilon` should be greater than 0.")

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_bounds_std_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    std_builder(parent_ds, Query(median=Query.Median())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_std_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    @staticmethod
    async def call(  # type: ignore[override]
        parent_ds: st.Dataset,
        axis: t.Optional[pdt.Axis] = 0,
        skipna: bool = True,
        level: t.Optional[pdt.Level] = None,
        numeric_only: t.Optional[bool] = None,
        ddof: int = 1,
        budget: t.Optional[st.Scalar] = None,
        seed: t.Optional[st.Scalar] = None,
        **kwargs: t.Any,
    ) -> t.Any:
        # Evaluate arguments
        (
            (dataframe, budget_value, seed_value),
            _,
            pe,
        ) = await arguments_values_and_protected_entity(
            parent_ds, budget, seed
        )

        assert type(dataframe) in [pd.DataFrame, pd.Series]
        assert pe.shape[0] == dataframe.shape[0]
        assert numeric_only
        assert axis == 0
        assert level is None
        assert seed_value
        assert budget_value

        _, tasks = await pd_std_dp.private_queries_and_task(
            parent_ds=parent_ds,
            budget=budget_value,
        )
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, std_tasks = tasks[0], tasks[1:]

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))

        # Compute DP value
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        std_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            df = dataframe[[column_name]].join(pe)
            subtasks = [unwrap(task) for task in std_tasks[index].subtasks]
            bounds_parameters, std_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    std_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
                df = df.dropna()
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            std_op = StdOp(
                parent_ds,
                std_parameters.parameters['noise_mean'],
                std_parameters.parameters['noise_square'],
                std_parameters.parameters['noise_count'],
            )
            std_dp_dict[column_name] = std_op.value(
                column_name, max_mul, bounds, random_generator
            )

        std_dp = pd.Series(std_dp_dict)
        return std_dp
