from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.refresh_json_web_token import RefreshJSONWebToken
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: RefreshJSONWebToken,
) -> Dict[str, Any]:
    url = "{}/api-token-refresh/".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[RefreshJSONWebToken]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = RefreshJSONWebToken.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[RefreshJSONWebToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RefreshJSONWebToken,
) -> Response[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Returns:
        Response[RefreshJSONWebToken]
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
    json_body: RefreshJSONWebToken,
) -> Optional[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Returns:
        Response[RefreshJSONWebToken]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: RefreshJSONWebToken,
) -> Response[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Returns:
        Response[RefreshJSONWebToken]
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
    json_body: RefreshJSONWebToken,
) -> Optional[RefreshJSONWebToken]:
    """API View that returns a refreshed token (with new expiration) based on
    existing token

     If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token

    Args:
        json_body (RefreshJSONWebToken):

    Returns:
        Response[RefreshJSONWebToken]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
