from typing import Any, Dict, List, Optional, Union

import requests

from ...client import Client
from ...models.paginated_product_stream_list import PaginatedProductStreamList
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {
    "active": str,
    "channels": str,
    "exclude_fields": List[str],
    "include_fields": List[str],
    "limit": int,
    "name": str,
    "offset": int,
    "product_streams": str,
    "product_variants": str,
    "product_versions": str,
    "products": str,
    "re_name": str,
    "re_ofuri": str,
    "search": str,
    "tags": int,
}


def _get_kwargs(
    *,
    client: Client,
    active: Union[Unset, None, str] = UNSET,
    channels: Union[Unset, None, str] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    product_streams: Union[Unset, None, str] = UNSET,
    product_variants: Union[Unset, None, str] = UNSET,
    product_versions: Union[Unset, None, str] = UNSET,
    products: Union[Unset, None, str] = UNSET,
    re_name: Union[Unset, None, str] = UNSET,
    re_ofuri: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/product_streams".format(
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

    params: Dict[str, Any] = {
        "active": active,
        "channels": channels,
        "exclude_fields": json_exclude_fields,
        "include_fields": json_include_fields,
        "limit": limit,
        "name": name,
        "offset": offset,
        "product_streams": product_streams,
        "product_variants": product_variants,
        "product_versions": product_versions,
        "products": products,
        "re_name": re_name,
        "re_ofuri": re_ofuri,
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
) -> Optional[PaginatedProductStreamList]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: PaginatedProductStreamList
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = PaginatedProductStreamList.from_dict(_response_200)

        return response_200
    return None


def _build_response(
    *, response: requests.Response
) -> Response[PaginatedProductStreamList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    active: Union[Unset, None, str] = UNSET,
    channels: Union[Unset, None, str] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    product_streams: Union[Unset, None, str] = UNSET,
    product_variants: Union[Unset, None, str] = UNSET,
    product_versions: Union[Unset, None, str] = UNSET,
    products: Union[Unset, None, str] = UNSET,
    re_name: Union[Unset, None, str] = UNSET,
    re_ofuri: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
) -> Response[PaginatedProductStreamList]:
    kwargs = _get_kwargs(
        client=client,
        active=active,
        channels=channels,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        name=name,
        offset=offset,
        product_streams=product_streams,
        product_variants=product_variants,
        product_versions=product_versions,
        products=products,
        re_name=re_name,
        re_ofuri=re_ofuri,
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
    active: Union[Unset, None, str] = UNSET,
    channels: Union[Unset, None, str] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    product_streams: Union[Unset, None, str] = UNSET,
    product_variants: Union[Unset, None, str] = UNSET,
    product_versions: Union[Unset, None, str] = UNSET,
    products: Union[Unset, None, str] = UNSET,
    re_name: Union[Unset, None, str] = UNSET,
    re_ofuri: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
) -> Optional[PaginatedProductStreamList]:
    """View for api/v1/product_streams"""

    return sync_detailed(
        client=client,
        active=active,
        channels=channels,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        name=name,
        offset=offset,
        product_streams=product_streams,
        product_variants=product_variants,
        product_versions=product_versions,
        products=products,
        re_name=re_name,
        re_ofuri=re_ofuri,
        search=search,
        tags=tags,
    ).parsed
