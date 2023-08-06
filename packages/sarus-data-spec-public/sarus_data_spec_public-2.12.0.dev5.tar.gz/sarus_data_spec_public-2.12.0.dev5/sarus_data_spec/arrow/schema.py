import typing as t

import pyarrow as pa

from sarus_data_spec.constants import DATA, PUBLIC, USER_COLUMN, WEIGHTS
from sarus_data_spec.type import Struct, Type
import sarus_data_spec.arrow.type as arrow_type
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


def to_arrow(schema: sp.Schema) -> pa.schema:
    """Convert Sarus schema to pyarrow schema."""
    return arrow_schema(Type(schema.type))


def arrow_schema(_type: st.Type) -> pa.Schema:
    """Visitor that returns the schema Arrow given the Sarus Type
    #TODO: Currently only Struct and Unions are supported
    """

    class SchemaVisitor(st.TypeVisitor):
        schema: pa.Schema = pa.schema(fields=[])

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.schema = pa.schema(
                fields=[
                    pa.field(
                        name=field_name,
                        type=arrow_type.to_arrow(fields[field_name]),
                    )
                    for field_name in fields.keys()
                ]
            )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # TODO
            pass

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # TODO
            pass

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            arrow_fields = [
                pa.field(
                    name=field_name,
                    type=arrow_type.to_arrow(field_type),
                )
                for field_name, field_type in fields.items()
            ]
            arrow_fields.append(
                pa.field(name='field_selected', type=pa.string())
            )
            self.schema = pa.schema(fields=arrow_fields)

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

    visitor = SchemaVisitor()
    _type.accept(visitor)
    return visitor.schema


def has_protected_format(schema: pa.Schema) -> bool:
    """Checks if the pyarrow schema corresponds to the Sarus protected
    format."""
    return set(schema.names) == {DATA, USER_COLUMN, WEIGHTS, PUBLIC}


def type_from_arrow_schema(schema: pa.Schema) -> st.Type:
    """Convert a Pyarrow schema to a Sarus Type.

    NB:
      - This does not handle the multitable case.
      - We need to handle differently the protected schema case because we
        cannot easily explore the StructType with Pyarrow < 10
    """
    if has_protected_format(schema):
        # TODO Remove this case when we have Pyarrow >= 10.0

        def normalize_field_name(field_name: str) -> str:
            """When flattening the fields, the field name becomes
            `data.field_name`."""
            return field_name[(len(DATA) + 1) :]

        data_fields = {
            normalize_field_name(field.name): arrow_type.type_from_arrow(
                field.type, nullable=False
            )
            for field in schema.field(DATA).flatten()
        }
        fields = {
            name: arrow_type.type_from_arrow(data_type, nullable=False)
            for name, data_type in zip(schema.names, schema.types)
            if name != DATA
        }
        fields[DATA] = Struct(fields=data_fields)
    else:
        fields = {
            name: arrow_type.type_from_arrow(data_type, nullable=False)
            for name, data_type in zip(schema.names, schema.types)
        }

    return Struct(fields=fields)
