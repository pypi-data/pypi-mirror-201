from typing import Dict, Any, Optional, List

from algora.api.service.object_metadata.__util import (
    _get_object_metadata_request_info,
    _get_all_object_metadata_request_info,
    _create_object_metadata_request_info,
    _update_object_metadata_request_info,
    _delete_object_metadata_request_info,
    _search_object_metadata_request_info,
)
from algora.api.service.object_metadata.enum import MetadataType
from algora.api.service.object_metadata.model import ObjectMetadataRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request(transformers=[no_transform])
def get_object_metadata(id: str) -> Dict[str, Any]:
    """
    Get object metadata by ID.

    Parameters:
        id (str): The object metadata id

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _get_object_metadata_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_all_object_metadata(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Get all the object metadata.

    Parameters:
        version (Optional[str]): The object metadata sdk version

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _get_all_object_metadata_request_info(version)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def create_object_metadata(request: ObjectMetadataRequest) -> Dict[str, Any]:
    """
    Create an object metadata.

    Parameters:
        request (ObjectMetadataRequest): The object metadata request

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _create_object_metadata_request_info(request)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_object_metadata(id: str, request: ObjectMetadataRequest) -> Dict[str, Any]:
    """
    Update an object metadata.

    Parameters:
        id (str): The object metadata id
        request (ObjectMetadataRequest): The object metadata request

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _update_object_metadata_request_info(id, request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform], processor=lambda r: r)
def delete_object_metadata(id: str) -> None:
    """
    Delete an object metadata.

    Parameters:
        id (str): The object metadata id

    Returns:
        None
    """
    request_info = _delete_object_metadata_request_info(id)
    return __delete_request(**request_info)


@data_request(transformers=[no_transform])
def search_object_metadata(
    class_name: Optional[str] = None,
    module: Optional[str] = None,
    path: Optional[str] = None,
    version: Optional[str] = None,
    type: Optional[MetadataType] = None,
    parent_class: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for object metadata.

    Parameters:
        class_name (Optional[str]): The object metadata class name
        module (Optional[str]): The object metadata module
        path (Optional[str]): The object metadata path
        version (Optional[str]): The object metadata sdk version
        type (Optional[str]): The object metadata type
        parent_class (Optional[str]): The object metadata parent_class

    Returns:
        List[Dict[str, Any]]: All of the object metadata that meets the search criteria
    """
    request_info = _search_object_metadata_request_info(
        class_name, module, path, version, type, parent_class
    )
    return __get_request(**request_info)
