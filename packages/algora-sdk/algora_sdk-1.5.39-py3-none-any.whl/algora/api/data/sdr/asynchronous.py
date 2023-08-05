from pandas import DataFrame

from algora.api.data.query import _async_query_timeseries
from algora.api.data.query.model import TimeseriesQueryRequest
from algora.api.data.sdr.__util import (
    _commodity_request_info,
)
from algora.common.decorators import async_data_request


@async_data_request
async def async_commodity(request: TimeseriesQueryRequest):
    """
    Asynchronously get SDR Commodity dataset.

    Args:
        request (TimeseriesQueryRequest): Dataset timeseries query

    Returns:
        DataFrame: DataFrame
    """
    request = _commodity_request_info(request)
    return await _async_query_timeseries(request)
