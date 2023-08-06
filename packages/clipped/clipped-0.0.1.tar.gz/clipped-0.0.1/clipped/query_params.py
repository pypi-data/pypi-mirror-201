from typing import Dict, Optional


def get_query_params(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    query: Optional[str] = None,
    sort: Optional[str] = None,
) -> Dict:
    params = {}
    if limit:
        params["limit"] = limit
    if offset:
        params["offset"] = offset
    if query:
        params["query"] = query
    if sort:
        params["sort"] = sort

    return params


def get_logs_params(
    last_time: Optional[str] = None, last_file: Optional[str] = None
) -> Dict:
    params = {}
    if last_file:
        params["last_file"] = last_file
    if last_time:
        params["last_time"] = last_time

    return params
