"""
Common models.
"""
from datetime import datetime
from typing import Optional
from pydantic import Field as pyField

from algora.common.base import Base
from algora.common.enum import FieldType
from algora.common.type import Datetime
from algora.quant.instrument.common.cut import BaseObservationCut


class Field(Base):
    logical_name: str
    type: FieldType


class DataDefinition(Base):
    """
    Base data definition.
    """

    cut: Optional[BaseObservationCut] = pyField(default=None)


class DataRequest(Base):
    """
    Base data request, inherited by all instrument-specific data request classes.
    """

    _sub_types_ = {}

    as_of_date: Optional[Datetime] = pyField(default=None)
    start_date: Optional[datetime] = pyField(default=None)
    end_date: Optional[datetime] = pyField(default=None)
    as_of: Optional[datetime] = pyField(default=None)

    def __init_subclass__(cls):
        data_definitions = [
            base for base in cls.__bases__ if issubclass(base, DataDefinition)
        ]
        if len(data_definitions) == 0:
            # Should I raise a InvalidClassDefinition exception if a data definition is missing?
            return

        data_definition_key = data_definitions[0].cls_name()
        cls._sub_types_[data_definition_key] = cls

    def create(self, data_definition: DataDefinition):
        klass = self._sub_types_.get(data_definition.cls_name(), None)
        if klass is None:
            raise TypeError()

        kwargs = self.request_dict()
        kwargs.update(data_definition.request_dict())
        return klass(**kwargs)
