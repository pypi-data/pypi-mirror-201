from typing import Any, Dict, List, Optional, Union

import requests

from ...client import Client
from ...models.paginated_channel_list import PaginatedChannelList
from ...models.v1_channels_list_type import V1ChannelsListType
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {
    "exclude_fields": List[str],
    "include_fields": List[str],
    "limit": int,
    "name": str,
    "offset": int,
    "search": str,
    "type": V1ChannelsListType,
}


def _get_kwargs(
    *,
    client: Client,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, V1ChannelsListType] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/channels".format(
        client.base_url,
    )

    headers: Dict[str, Any] = client.get_headers()

    json_exclude_fields: Union[Unset, None, List[str]] = UNSET
    if not isinstance(exclude_fields, Unset):
        if exclude_fields is None:
            json_exclude_fields = None
        else:
            json_exclude_fields = exclude_fields

    json_include_fields: Union[Unset, None, List[str]] = UNSET
    if not isinstance(include_fields, Unset):
        if include_fields is None:
            json_include_fields = None
        else:
            json_include_fields = include_fields

    json_type: Union[Unset, None, str] = UNSET
    if not isinstance(type, Unset):

        json_type = V1ChannelsListType(type).value if type else None

    params: Dict[str, Any] = {
        "exclude_fields": json_exclude_fields,
        "include_fields": json_include_fields,
        "limit": limit,
        "name": name,
        "offset": offset,
        "search": search,
        "type": json_type,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "params": params,
    }


def _parse_response(*, response: requests.Response) -> Optional[PaginatedChannelList]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: PaginatedChannelList
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = PaginatedChannelList.from_dict(_response_200)

        return response_200
    return None


def _build_response(*, response: requests.Response) -> Response[PaginatedChannelList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, V1ChannelsListType] = UNSET,
) -> Response[PaginatedChannelList]:
    kwargs = _get_kwargs(
        client=client,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        name=name,
        offset=offset,
        search=search,
        type=type,
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
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, V1ChannelsListType] = UNSET,
) -> Optional[PaginatedChannelList]:
    """View for api/v1/channels"""

    return sync_detailed(
        client=client,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        name=name,
        offset=offset,
        search=search,
        type=type,
    ).parsed
