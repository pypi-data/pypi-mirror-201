import pandas as pd
from requests import Response

from algora.api.data.query.__util import (
    _query_dataset_csv_request_info,
    _query_timeseries_request_info,
    _query_distinct_fields_request_info,
)
from algora.api.data.query.model import TimeseriesQueryRequest, DistinctQueryRequest
from algora.common.decorators import data_request
from algora.common.requests import __get_request, __post_request


def _query_timeseries(request: TimeseriesQueryRequest):
    """
    Query timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        Response: Response
    """
    request_info = _query_timeseries_request_info(request)
    return __post_request(**request_info)


def _query_distinct_fields(request: DistinctQueryRequest):
    """
    Query dataset for distinct values of a specified field.

    Args:
        request (DistinctQueryRequest): Distinct query request

    Returns:
        Response: Response
    """
    request_info = _query_distinct_fields_request_info(request)
    return __post_request(**request_info)


@data_request
def query_timeseries(request: TimeseriesQueryRequest) -> pd.DataFrame:
    """
    Query timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    return _query_timeseries(request)


def query_dataset_csv(id: str, request: TimeseriesQueryRequest) -> Response:
    """
    Query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, request)
    return __get_request(**request_info)


@data_request
def query_distinct_fields(request: DistinctQueryRequest) -> pd.DataFrame:
    """
    Query dataset for distinct values of a specified field.

    Args:
        request (DistinctQueryRequest): Distinct query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    return _query_distinct_fields(request)
