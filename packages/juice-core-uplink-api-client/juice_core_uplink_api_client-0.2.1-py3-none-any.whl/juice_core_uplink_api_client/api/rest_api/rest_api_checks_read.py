from http import HTTPStatus
from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    working_group_mnemonic: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest_api/checks/{working_group_mnemonic}/".format(
        client.base_url, working_group_mnemonic=working_group_mnemonic
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    working_group_mnemonic: str,
    *,
    client: Client,
) -> Response[Any]:
    """Checks the segment definition completeness of working group

     Checks the segment definition completeness of working group

    Args:
        working_group_mnemonic (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        working_group_mnemonic=working_group_mnemonic,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    working_group_mnemonic: str,
    *,
    client: Client,
) -> Response[Any]:
    """Checks the segment definition completeness of working group

     Checks the segment definition completeness of working group

    Args:
        working_group_mnemonic (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        working_group_mnemonic=working_group_mnemonic,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
