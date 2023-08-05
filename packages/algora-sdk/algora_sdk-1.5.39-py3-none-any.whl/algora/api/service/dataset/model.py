from typing import Optional, List, Dict, Any
from pydantic import Field as pyField

from algora.api.data.query.model import WhereClause
from algora.common.base import Base
from algora.common.enum import Order, FieldType


class Field(Base):
    display_name: str
    logical_name: str
    type: FieldType
    width: int
    editable: bool
    hidden: bool
    display_order: int
    tags: List[str]
    field_group_display_name: str
    field_group_logical_name: str


class DatasetRequest(Base):
    reference_name: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: Optional[List[str]]
    where_clause: Optional[WhereClause]
    row_limit: Optional[int]
    max_limit: Optional[int]
    sort: Optional[Dict[str, Order]]
    abstract_dataset_id: str
    schema_: List[Field] = pyField(alias="schema")


class DatasetResponse(Base):
    id: str
    reference_name: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: List[str]
    where_clause: Optional[WhereClause]
    row_limit: Optional[int]
    max_limit: Optional[int]
    sort: Dict[str, Order]
    abstract_dataset_id: str
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
    schema_: List[Field] = pyField(alias="schema")


class SearchRequest(Base):
    query: str
