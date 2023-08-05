from algora.api.data.query.model import TimeseriesQueryRequest, DistinctQueryRequest


def _query_timeseries_request_info(request: TimeseriesQueryRequest) -> dict:
    return {"endpoint": f"data/timeseries", "json": request.request_dict()}


def _query_dataset_csv_request_info(id: str, request: TimeseriesQueryRequest) -> dict:
    return {"endpoint": f"data/{id}.csv", "json": request.request_dict()}


def _query_distinct_fields_request_info(request: DistinctQueryRequest) -> dict:
    return {"endpoint": f"data/distinct", "json": request.request_dict()}
