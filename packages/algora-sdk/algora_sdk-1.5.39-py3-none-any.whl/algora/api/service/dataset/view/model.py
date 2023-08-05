from typing import Optional, List, Dict
from pydantic import Field as pyField

from algora.api.data.query.model import WhereClause
from algora.api.service.dataset.model import Field
from algora.common.base import Base
from algora.common.enum import Order


class DatasetViewResponse(Base):
    id: str
    reference_name: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: List[str]
    where_clause: Optional[WhereClause]
    row_limit: int
    max_limit: int
    sort: Dict[str, Order]
    abstract_dataset_id: str
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
    schema_: List[Field] = pyField(alias="schema")
