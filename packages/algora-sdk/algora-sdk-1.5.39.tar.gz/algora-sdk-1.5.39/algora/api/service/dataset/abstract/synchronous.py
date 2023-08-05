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
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request(transformers=[no_transform])
def get_abstract_dataset(id: str) -> Dict[str, Any]:
    """
    Get abstract dataset by ID.

    Args:
        id (str): Abstract dataset ID

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _get_abstract_dataset_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_abstract_datasets() -> List[Dict[str, Any]]:
    """
    Get all abstract datasets.

    Returns:
        List[Dict[str, Any]]: List of abstract dataset response
    """
    request_info = _get_abstract_datasets_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def search_abstract_datasets(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all abstract datasets.

    Args:
        request (SearchRequest): Abstract dataset search request

    Returns:
        List[Dict[str, Any]]: List of abstract dataset response
    """
    request_info = _search_abstract_datasets_request_info(request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def create_abstract_dataset(request: AbstractDatasetRequest) -> Dict[str, Any]:
    """
    Create abstract dataset.

    Args:
        request (DatasetRequest): Abstract dataset request

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _create_abstract_dataset_request_info(request)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_abstract_dataset(id: str, request: AbstractDatasetRequest) -> Dict[str, Any]:
    """
    Update abstract dataset.

    Args:
        id (str): Abstract dataset ID
        request (DatasetRequest): Abstract dataset request

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _update_abstract_dataset_request_info(id, request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def delete_abstract_dataset(id: str) -> None:
    """
    Delete abstract dataset by ID.

    Args:
        id (str): Abstract dataset ID

    Returns:
        None
    """
    request_info = _delete_abstract_dataset_request_info(id)
    return __delete_request(**request_info)
