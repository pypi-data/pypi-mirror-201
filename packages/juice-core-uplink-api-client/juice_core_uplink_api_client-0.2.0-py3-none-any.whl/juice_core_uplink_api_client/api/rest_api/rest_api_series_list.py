from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.series_data import SeriesData
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    body: str,
) -> Dict[str, Any]:
    url = "{}/rest_api/series/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["body"] = body

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List["SeriesData"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SeriesData.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List["SeriesData"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: str,
) -> Response[Union[Any, List["SeriesData"]]]:
    """Retrieve a geometry series of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * series: the name of the series to be retrieved

    Args:
        body (str):

    Returns:
        Response[Union[Any, List['SeriesData']]]
    """

    kwargs = _get_kwargs(
        client=client,
        body=body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    body: str,
) -> Optional[Union[Any, List["SeriesData"]]]:
    """Retrieve a geometry series of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * series: the name of the series to be retrieved

    Args:
        body (str):

    Returns:
        Response[Union[Any, List['SeriesData']]]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: str,
) -> Response[Union[Any, List["SeriesData"]]]:
    """Retrieve a geometry series of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * series: the name of the series to be retrieved

    Args:
        body (str):

    Returns:
        Response[Union[Any, List['SeriesData']]]
    """

    kwargs = _get_kwargs(
        client=client,
        body=body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    body: str,
) -> Optional[Union[Any, List["SeriesData"]]]:
    """Retrieve a geometry series of a trajectory

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * trajectory: the name of the trajectory
    * series: the name of the series to be retrieved

    Args:
        body (str):

    Returns:
        Response[Union[Any, List['SeriesData']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
