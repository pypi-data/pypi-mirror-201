from typing import Optional, List, Dict
from pydantic import Field as pyField

from algora.api.data.query.model import WhereClause
from algora.api.service.dataset.model import Field
from algora.common.enum import Order
from algora.common.base import Base


class AbstractDatasetRequest(Base):
    dataset_name: str
    display_name: str
    description: Optional[str]
    table_name: str
    where_clause: Optional[WhereClause]
    row_limit: int
    max_limit: int
    sort: Dict[str, Order]
    tags: List[str]
    schema_: List[Field] = pyField(alias="schema")


class AbstractDatasetResponse(Base):
    id: str
    dataset_name: str
    display_name: str
    description: Optional[str]
    table_name: str
    where_clause: Optional[WhereClause]
    row_limit: int
    max_limit: int
    sort: Dict[str, Order]
    tags: List[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
    schema_: List[Field] = pyField(alias="schema")
