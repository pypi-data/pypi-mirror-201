from typing import Dict, Any, Optional

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
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request(transformers=[no_transform])
async def async_get_object_metadata(id: str) -> Dict[str, Any]:
    """
    Asynchronously get object metadata by ID.

    Parameters:
        id (str): The object metadata id

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _get_object_metadata_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_all_object_metadata(
    version: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Asynchronously get all the object metadata.

    Parameters:
        version (Optional[str]): The object metadata sdk version

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _get_all_object_metadata_request_info(version)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_object_metadata(
    request: ObjectMetadataRequest,
) -> Dict[str, Any]:
    """
    Asynchronously create an object metadata.

    Parameters:
        request (ObjectMetadataRequest): The object metadata request

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _create_object_metadata_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_object_metadata(
    id: str, request: ObjectMetadataRequest
) -> Dict[str, Any]:
    """
    Asynchronously update an object metadata.

    Parameters:
        id (str): The object metadata id
        request (ObjectMetadataRequest): The object metadata request

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _update_object_metadata_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform], processor=lambda r: r)
async def async_delete_object_metadata(id: str) -> None:
    """
    Asynchronously delete an object metadata.

    Parameters:
        id (str): The object metadata id

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _delete_object_metadata_request_info(id)
    return await __async_delete_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_search_object_metadata(
    class_name: Optional[str] = None,
    module: Optional[str] = None,
    path: Optional[str] = None,
    version: Optional[str] = None,
    type: Optional[MetadataType] = None,
    parent_class: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Asynchronously search for an object metadata.

    Parameters:
        class_name (Optional[str]): The object metadata class name
        module (Optional[str]): The object metadata module
        path (Optional[str]): The object metadata path
        version (Optional[str]): The object metadata sdk version
        type (Optional[str]): The object metadata type
        parent_class (Optional[str]): The object metadata parent_class

    Returns:
        Dict[str, Any]: Object metadata response
    """
    request_info = _search_object_metadata_request_info(
        class_name, module, path, version, type, parent_class
    )
    return await __async_get_request(**request_info)
