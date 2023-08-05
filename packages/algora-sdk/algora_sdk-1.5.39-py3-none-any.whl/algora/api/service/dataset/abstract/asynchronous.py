from typing import Dict, Any, List

from algora.api.service.dataset.abstract.__util import (
    _get_abstract_dataset_request_info,
    _get_abstract_datasets_request_info,
    _search_abstract_datasets_request_info,
    _create_abstract_dataset_request_info,
    _update_abstract_dataset_request_info,
    _delete_abstract_dataset_request_info,
)
from algora.api.service.dataset.abstract.model import AbstractDatasetRequest
from algora.api.service.dataset.model import SearchRequest
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request(transformers=[no_transform])
async def async_get_abstract_dataset(id: str) -> Dict[str, Any]:
    """
    Asynchronously get abstract dataset by ID.

    Args:
        id (str): Abstract dataset ID

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _get_abstract_dataset_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_abstract_datasets() -> List[Dict[str, Any]]:
    """
    Asynchronously get all abstract datasets.

    Returns:
        List[Dict[str, Any]]: List of abstract dataset response
    """
    request_info = _get_abstract_datasets_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_search_abstract_datasets(
    request: SearchRequest,
) -> List[Dict[str, Any]]:
    """
    Asynchronously search all abstract datasets.

    Args:
        request (SearchRequest): Abstract dataset search request

    Returns:
        List[Dict[str, Any]]: List of abstract dataset response
    """
    request_info = _search_abstract_datasets_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_abstract_dataset(
    request: AbstractDatasetRequest,
) -> Dict[str, Any]:
    """
    Asynchronously create abstract dataset.

    Args:
        request (AbstractDatasetRequest): Abstract dataset request

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _create_abstract_dataset_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_abstract_dataset(
    id: str, request: AbstractDatasetRequest
) -> Dict[str, Any]:
    """
    Asynchronously update abstract dataset.

    Args:
        id (str): Abstract dataset ID
        request (AbstractDatasetRequest): Abstract dataset request

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _update_abstract_dataset_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_delete_abstract_dataset(id: str) -> None:
    """
    Asynchronously delete abstract dataset by ID.

    Args:
        id (str): Abstract dataset ID

    Returns:
        None
    """
    request_info = _delete_abstract_dataset_request_info(id)
    return await __async_delete_request(**request_info)
