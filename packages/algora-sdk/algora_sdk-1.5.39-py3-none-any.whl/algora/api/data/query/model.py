"""
Data classes for API requests.
"""
from typing import List, Optional, Any

from pydantic import Field

from algora.common.base import Base
from algora.common.enum import Order, SqlOperator, BooleanOperator


class Sort(Base):
    field: str
    order: Order


class Filter(Base):
    field: str
    operator: SqlOperator
    value: Any


class WhereClause(Base):
    filter: Optional[Filter] = Field(default=None)
    operator: Optional[BooleanOperator] = Field(default=None)
    left: Optional["WhereClause"] = Field(default=None)
    right: Optional["WhereClause"] = Field(default=None)


class TimeseriesQueryRequest(Base):
    id: Optional[str] = Field(default=None)
    dataset_name: Optional[str] = Field(default=None)
    reference_name: Optional[str] = Field(default=None)
    page: Optional[int] = Field(default=None)
    limit: Optional[int] = Field(default=None)
    fields: Optional[List[str]] = Field(default=None)
    sort: Optional[List[Sort]] = Field(default=None)
    where: Optional[WhereClause] = Field(default=None)


class DistinctQueryRequest(Base):
    id: Optional[str] = Field(default=None)
    dataset_name: Optional[str] = Field(default=None)
    reference_name: Optional[str] = Field(default=None)
    field: str = Field(default=None)
