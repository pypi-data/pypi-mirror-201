from typing import Any, Dict, Optional, Union

import requests

from ...client import Client
from ...models.v1_status_list_response_200 import V1StatusListResponse200
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {
    "limit": int,
    "offset": int,
}


def _get_kwargs(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/status".format(
        client.base_url,
    )

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "limit": limit,
        "offset": offset,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "params": params,
    }


def _parse_response(
    *, response: requests.Response
) -> Optional[V1StatusListResponse200]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: V1StatusListResponse200
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = V1StatusListResponse200.from_dict(_response_200)

        return response_200
    return None


def _build_response(
    *, response: requests.Response
) -> Response[V1StatusListResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
) -> Response[V1StatusListResponse200]:
    kwargs = _get_kwargs(
        client=client,
        limit=limit,
        offset=offset,
    )

    response = requests.get(
        verify=client.verify_ssl,
        auth=client.auth,
        timeout=client.timeout,
        **kwargs,
    )
    response.raise_for_status()

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
) -> Optional[V1StatusListResponse200]:
    """ """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed
