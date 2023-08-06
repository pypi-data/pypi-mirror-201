from typing import Dict, Optional

try:
    import requests
except ImportError:
    raise ImportError("This module depends on requests.")


def safe_request(
    url: str,
    method: str = None,
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    allow_redirects: bool = False,
    timeout: int = 30,
    verify_ssl: bool = True,
) -> requests.Response:
    """A slightly safer version of `request`."""

    session = requests.Session()

    kwargs = {}

    if json:
        kwargs["json"] = json
        if not headers:
            headers = {}
        headers.setdefault("Content-Type", "application/json")

    if data:
        kwargs["data"] = data

    if params:
        kwargs["params"] = params

    if headers:
        kwargs["headers"] = headers

    if method is None:
        method = "POST" if (data or json) else "GET"

    response = session.request(
        method=method,
        url=url,
        allow_redirects=allow_redirects,
        timeout=timeout,
        verify=verify_ssl,
        **kwargs
    )

    return response
