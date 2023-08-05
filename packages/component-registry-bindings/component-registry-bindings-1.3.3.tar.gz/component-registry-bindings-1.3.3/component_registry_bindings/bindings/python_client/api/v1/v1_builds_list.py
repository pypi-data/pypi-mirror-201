from typing import Any, Dict, List, Optional, Union

import requests

from ...client import Client
from ...models.paginated_software_build_list import PaginatedSoftwareBuildList
from ...models.v1_builds_list_build_type import V1BuildsListBuildType
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {
    "build_type": V1BuildsListBuildType,
    "exclude_fields": List[str],
    "include_fields": List[str],
    "limit": int,
    "name": str,
    "offset": int,
    "search": str,
    "tags": int,
}


def _get_kwargs(
    *,
    client: Client,
    build_type: Union[Unset, None, V1BuildsListBuildType] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/builds".format(
        client.base_url,
    )

    headers: Dict[str, Any] = client.get_headers()

    json_build_type: Union[Unset, None, str] = UNSET
    if not isinstance(build_type, Unset):

        json_build_type = (
            V1BuildsListBuildType(build_type).value if build_type else None
        )

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

    params: Dict[str, Any] = {
        "build_type": json_build_type,
        "exclude_fields": json_exclude_fields,
        "include_fields": json_include_fields,
        "limit": limit,
        "name": name,
        "offset": offset,
        "search": search,
        "tags": tags,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "params": params,
    }


def _parse_response(
    *, response: requests.Response
) -> Optional[PaginatedSoftwareBuildList]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: PaginatedSoftwareBuildList
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = PaginatedSoftwareBuildList.from_dict(_response_200)

        return response_200
    return None


def _build_response(
    *, response: requests.Response
) -> Response[PaginatedSoftwareBuildList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    build_type: Union[Unset, None, V1BuildsListBuildType] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
) -> Response[PaginatedSoftwareBuildList]:
    kwargs = _get_kwargs(
        client=client,
        build_type=build_type,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        name=name,
        offset=offset,
        search=search,
        tags=tags,
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
    build_type: Union[Unset, None, V1BuildsListBuildType] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
) -> Optional[PaginatedSoftwareBuildList]:
    """View for api/v1/builds"""

    return sync_detailed(
        client=client,
        build_type=build_type,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        name=name,
        offset=offset,
        search=search,
        tags=tags,
    ).parsed
