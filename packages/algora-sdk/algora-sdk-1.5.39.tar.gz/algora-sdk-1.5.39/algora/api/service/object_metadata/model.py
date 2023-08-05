from typing import Dict, Any, Set, Optional, List, Union
from pydantic import Field

from algora.api.service.object_metadata.enum import MetadataType, Type, PythonTypes
from algora.common.base import Base


class TypeInfo(Base):
    kind: Type
    type: Union[str, PythonTypes]
    sub_types: List["TypeInfo"] = Field(default_factory=list)


class Parameter(Base):
    name: str
    position: int
    type: Optional[TypeInfo] = None
    default: Optional[Any] = None
    options: Optional[List[Any]] = None


class ObjectMetadataRequest(Base):
    class_name: str
    module: str
    path: str
    version: str
    type: MetadataType
    constructor_parameters: Dict[str, Parameter]
    parent_classes: Optional[Set[str]]
    docs: Optional[str]


class ObjectMetadataResponse(Base):
    class_name: str
    module: str
    path: str
    version: str
    type: MetadataType
    constructor_parameters: Dict[str, Parameter]
    parent_classes: Optional[Set[str]]
    docs: Optional[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
