from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.engineering_segment import EngineeringSegment
from ...types import Response


def _get_kwargs(
    mnemonic: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest_api/trajectory/{mnemonic}/engineering_segments".format(client.base_url, mnemonic=mnemonic)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List["EngineeringSegment"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EngineeringSegment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List["EngineeringSegment"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    mnemonic: str,
    *,
    client: Client,
) -> Response[Union[Any, List["EngineeringSegment"]]]:
    """Retrieve the engineering segments belonging to the trajectory

     List all engineering segments of a trajectory

    Args:
        mnemonic (str):

    Returns:
        Response[Union[Any, List['EngineeringSegment']]]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    mnemonic: str,
    *,
    client: Client,
) -> Optional[Union[Any, List["EngineeringSegment"]]]:
    """Retrieve the engineering segments belonging to the trajectory

     List all engineering segments of a trajectory

    Args:
        mnemonic (str):

    Returns:
        Response[Union[Any, List['EngineeringSegment']]]
    """

    return sync_detailed(
        mnemonic=mnemonic,
        client=client,
    ).parsed


async def asyncio_detailed(
    mnemonic: str,
    *,
    client: Client,
) -> Response[Union[Any, List["EngineeringSegment"]]]:
    """Retrieve the engineering segments belonging to the trajectory

     List all engineering segments of a trajectory

    Args:
        mnemonic (str):

    Returns:
        Response[Union[Any, List['EngineeringSegment']]]
    """

    kwargs = _get_kwargs(
        mnemonic=mnemonic,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    mnemonic: str,
    *,
    client: Client,
) -> Optional[Union[Any, List["EngineeringSegment"]]]:
    """Retrieve the engineering segments belonging to the trajectory

     List all engineering segments of a trajectory

    Args:
        mnemonic (str):

    Returns:
        Response[Union[Any, List['EngineeringSegment']]]
    """

    return (
        await asyncio_detailed(
            mnemonic=mnemonic,
            client=client,
        )
    ).parsed
