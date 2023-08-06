from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.mode import Mode
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest_api/mode/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Mode]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Mode.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Mode]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Mode]:
    """Retrieve the list of modes

     Get the list of modes

    Returns:
        Response[Mode]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Mode]:
    """Retrieve the list of modes

     Get the list of modes

    Returns:
        Response[Mode]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Mode]:
    """Retrieve the list of modes

     Get the list of modes

    Returns:
        Response[Mode]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Mode]:
    """Retrieve the list of modes

     Get the list of modes

    Returns:
        Response[Mode]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
