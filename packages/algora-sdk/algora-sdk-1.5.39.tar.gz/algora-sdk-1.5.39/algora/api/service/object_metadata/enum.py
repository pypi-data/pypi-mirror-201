from typing import Union, Any, Optional

from algora.common.base_enum import BaseEnum


class MetadataType(BaseEnum):
    CLASS = "CLASS"
    ENUM = "ENUM"
    ABSTRACT_CLASS = "ABSTRACT_CLASS"


class Type(BaseEnum):
    BUILT_IN = "BUILT_IN"
    ALIAS = "ALIAS"
    REF = "REF"
    CUSTOM = "CUSTOM"
    UNSUPPORTED = "UNSUPPORTED"


class PythonTypes(BaseEnum):
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    NONE = "NONE"
    LIST = "LIST"
    SET = "SET"
    DICT = "DICT"
    UNION = "UNION"
    OPTIONAL = "OPTIONAL"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_type(cls, origin: Any, sub_types: Optional[Any] = None):
        value_lookup = {
            bool: "BOOLEAN",
            int: "INTEGER",
            float: "FLOAT",
            str: "STRING",
            type(None): "NONE",
            None: "NONE",
            list: "LIST",
            set: "SET",
            Union: "UNION",
            dict: "DICT",
        }
        value = value_lookup.get(origin, "UNKNOWN")
        if value == "UNION":
            value = cls.evaluate_union(origin, sub_types)
        return cls(value=value)

    @classmethod
    def evaluate_union(cls, origin: Any, sub_types: Optional[Any] = None):
        if sub_types and type(None) in sub_types:
            return "OPTIONAL"
        else:
            return "UNION"
