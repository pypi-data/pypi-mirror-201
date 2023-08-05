from algora.api.data.query.model import TimeseriesQueryRequest


def _commodity_request_info(request: TimeseriesQueryRequest):
    updated_request = request.copy(id="2880e242-8db4-49e2-aad3-e0339931582e")
    return updated_request
