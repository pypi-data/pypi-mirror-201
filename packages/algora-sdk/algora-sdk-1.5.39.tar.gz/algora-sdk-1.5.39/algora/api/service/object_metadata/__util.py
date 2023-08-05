from typing import Optional

from algora.api.service.object_metadata.enum import MetadataType
from algora.api.service.object_metadata.model import ObjectMetadataRequest


def _get_object_metadata_request_info(id: str) -> dict:
    return {"endpoint": f"config/object/metadata/{id}"}


def _get_all_object_metadata_request_info(version: Optional[str] = None) -> dict:
    params = {
        "version": version,
    }
    return {
        "endpoint": f"config/object/metadata",
        "params": {k: v for k, v in params.items() if v is not None},
    }


def _create_object_metadata_request_info(request: ObjectMetadataRequest) -> dict:
    return {"endpoint": f"config/object/metadata", "json": request.request_dict()}


def _update_object_metadata_request_info(
    id: str, request: ObjectMetadataRequest
) -> dict:
    return {
        "endpoint": f"config/object/metadata/{id}",
        "json": request.request_dict(),
    }


def _delete_object_metadata_request_info(id: str) -> dict:
    return {"endpoint": f"config/object/metadata/{id}"}


def _search_object_metadata_request_info(
    class_name: Optional[str] = None,
    module: Optional[str] = None,
    path: Optional[str] = None,
    version: Optional[str] = None,
    type: Optional[MetadataType] = None,
    parent_class: Optional[str] = None,
) -> dict:
    params = {
        "class_name": class_name,
        "module": module,
        "path": path,
        "version": version,
        "type": type,
        "parent_class": parent_class,
    }
    return {
        "endpoint": f"config/object/metadata/search",
        "params": {k: v for k, v in params.items() if v is not None},
    }
