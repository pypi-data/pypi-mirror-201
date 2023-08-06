from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.json_web_token import JSONWebToken
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: JSONWebToken,
) -> Dict[str, Any]:
    url = "{}/api-token-auth/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[JSONWebToken]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = JSONWebToken.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[JSONWebToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: JSONWebToken,
) -> Response[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Returns:
        Response[JSONWebToken]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: JSONWebToken,
) -> Optional[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Returns:
        Response[JSONWebToken]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: JSONWebToken,
) -> Response[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Returns:
        Response[JSONWebToken]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: JSONWebToken,
) -> Optional[JSONWebToken]:
    """API View that receives a POST with a user's username and password.

     Returns a JSON Web Token that can be used for authenticated requests.

    Args:
        json_body (JSONWebToken):

    Returns:
        Response[JSONWebToken]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
