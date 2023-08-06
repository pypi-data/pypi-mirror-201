from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.detailed_scenario import DetailedScenario
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: DetailedScenario,
) -> Dict[str, Any]:
    url = "{}/rest_api/detailed_scenario/".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, DetailedScenario]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = DetailedScenario.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, DetailedScenario]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: DetailedScenario,
) -> Response[Union[Any, DetailedScenario]]:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        json_body (DetailedScenario):

    Returns:
        Response[Union[Any, DetailedScenario]]
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
    json_body: DetailedScenario,
) -> Optional[Union[Any, DetailedScenario]]:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        json_body (DetailedScenario):

    Returns:
        Response[Union[Any, DetailedScenario]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: DetailedScenario,
) -> Response[Union[Any, DetailedScenario]]:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        json_body (DetailedScenario):

    Returns:
        Response[Union[Any, DetailedScenario]]
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
    json_body: DetailedScenario,
) -> Optional[Union[Any, DetailedScenario]]:
    """Adds a new detailed scenario

     Adds a new plan to the trajectory

    Args:
        json_body (DetailedScenario):

    Returns:
        Response[Union[Any, DetailedScenario]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
