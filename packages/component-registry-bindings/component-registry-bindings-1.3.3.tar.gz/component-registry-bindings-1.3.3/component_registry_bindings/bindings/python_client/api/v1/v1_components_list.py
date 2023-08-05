from typing import Any, Dict, List, Optional, Union

import requests

from ...client import Client
from ...models.paginated_component_list import PaginatedComponentList
from ...models.v1_components_list_namespace import V1ComponentsListNamespace
from ...models.v1_components_list_type import V1ComponentsListType
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {
    "arch": str,
    "channels": str,
    "description": str,
    "el_match": str,
    "exclude_fields": List[str],
    "include_fields": List[str],
    "limit": int,
    "missing_copyright": bool,
    "missing_license": bool,
    "name": str,
    "namespace": V1ComponentsListNamespace,
    "nevra": str,
    "nvr": str,
    "offset": int,
    "ofuri": str,
    "product_streams": str,
    "product_variants": str,
    "product_versions": str,
    "products": str,
    "provides": str,
    "purl": str,
    "re_name": str,
    "re_provides": str,
    "re_purl": str,
    "re_sources": str,
    "re_upstreams": str,
    "related_url": str,
    "release": str,
    "search": str,
    "sources": str,
    "tags": int,
    "type": V1ComponentsListType,
    "upstreams": str,
    "version": str,
    "view": str,
}


def _get_kwargs(
    *,
    client: Client,
    arch: Union[Unset, None, str] = UNSET,
    channels: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    el_match: Union[Unset, None, str] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    missing_copyright: Union[Unset, None, bool] = UNSET,
    missing_license: Union[Unset, None, bool] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    namespace: Union[Unset, None, V1ComponentsListNamespace] = UNSET,
    nevra: Union[Unset, None, str] = UNSET,
    nvr: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ofuri: Union[Unset, None, str] = UNSET,
    product_streams: Union[Unset, None, str] = UNSET,
    product_variants: Union[Unset, None, str] = UNSET,
    product_versions: Union[Unset, None, str] = UNSET,
    products: Union[Unset, None, str] = UNSET,
    provides: Union[Unset, None, str] = UNSET,
    purl: Union[Unset, None, str] = UNSET,
    re_name: Union[Unset, None, str] = UNSET,
    re_provides: Union[Unset, None, str] = UNSET,
    re_purl: Union[Unset, None, str] = UNSET,
    re_sources: Union[Unset, None, str] = UNSET,
    re_upstreams: Union[Unset, None, str] = UNSET,
    related_url: Union[Unset, None, str] = UNSET,
    release: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    sources: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, V1ComponentsListType] = UNSET,
    upstreams: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    view: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/components".format(
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

    json_namespace: Union[Unset, None, str] = UNSET
    if not isinstance(namespace, Unset):

        json_namespace = (
            V1ComponentsListNamespace(namespace).value if namespace else None
        )

    json_type: Union[Unset, None, str] = UNSET
    if not isinstance(type, Unset):

        json_type = V1ComponentsListType(type).value if type else None

    params: Dict[str, Any] = {
        "arch": arch,
        "channels": channels,
        "description": description,
        "el_match": el_match,
        "exclude_fields": json_exclude_fields,
        "include_fields": json_include_fields,
        "limit": limit,
        "missing_copyright": missing_copyright,
        "missing_license": missing_license,
        "name": name,
        "namespace": json_namespace,
        "nevra": nevra,
        "nvr": nvr,
        "offset": offset,
        "ofuri": ofuri,
        "product_streams": product_streams,
        "product_variants": product_variants,
        "product_versions": product_versions,
        "products": products,
        "provides": provides,
        "purl": purl,
        "re_name": re_name,
        "re_provides": re_provides,
        "re_purl": re_purl,
        "re_sources": re_sources,
        "re_upstreams": re_upstreams,
        "related_url": related_url,
        "release": release,
        "search": search,
        "sources": sources,
        "tags": tags,
        "type": json_type,
        "upstreams": upstreams,
        "version": version,
        "view": view,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "params": params,
    }


def _parse_response(*, response: requests.Response) -> Optional[PaginatedComponentList]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: PaginatedComponentList
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = PaginatedComponentList.from_dict(_response_200)

        return response_200
    return None


def _build_response(*, response: requests.Response) -> Response[PaginatedComponentList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    arch: Union[Unset, None, str] = UNSET,
    channels: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    el_match: Union[Unset, None, str] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    missing_copyright: Union[Unset, None, bool] = UNSET,
    missing_license: Union[Unset, None, bool] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    namespace: Union[Unset, None, V1ComponentsListNamespace] = UNSET,
    nevra: Union[Unset, None, str] = UNSET,
    nvr: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ofuri: Union[Unset, None, str] = UNSET,
    product_streams: Union[Unset, None, str] = UNSET,
    product_variants: Union[Unset, None, str] = UNSET,
    product_versions: Union[Unset, None, str] = UNSET,
    products: Union[Unset, None, str] = UNSET,
    provides: Union[Unset, None, str] = UNSET,
    purl: Union[Unset, None, str] = UNSET,
    re_name: Union[Unset, None, str] = UNSET,
    re_provides: Union[Unset, None, str] = UNSET,
    re_purl: Union[Unset, None, str] = UNSET,
    re_sources: Union[Unset, None, str] = UNSET,
    re_upstreams: Union[Unset, None, str] = UNSET,
    related_url: Union[Unset, None, str] = UNSET,
    release: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    sources: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, V1ComponentsListType] = UNSET,
    upstreams: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    view: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedComponentList]:
    kwargs = _get_kwargs(
        client=client,
        arch=arch,
        channels=channels,
        description=description,
        el_match=el_match,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        missing_copyright=missing_copyright,
        missing_license=missing_license,
        name=name,
        namespace=namespace,
        nevra=nevra,
        nvr=nvr,
        offset=offset,
        ofuri=ofuri,
        product_streams=product_streams,
        product_variants=product_variants,
        product_versions=product_versions,
        products=products,
        provides=provides,
        purl=purl,
        re_name=re_name,
        re_provides=re_provides,
        re_purl=re_purl,
        re_sources=re_sources,
        re_upstreams=re_upstreams,
        related_url=related_url,
        release=release,
        search=search,
        sources=sources,
        tags=tags,
        type=type,
        upstreams=upstreams,
        version=version,
        view=view,
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
    arch: Union[Unset, None, str] = UNSET,
    channels: Union[Unset, None, str] = UNSET,
    description: Union[Unset, None, str] = UNSET,
    el_match: Union[Unset, None, str] = UNSET,
    exclude_fields: Union[Unset, None, List[str]] = UNSET,
    include_fields: Union[Unset, None, List[str]] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    missing_copyright: Union[Unset, None, bool] = UNSET,
    missing_license: Union[Unset, None, bool] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    namespace: Union[Unset, None, V1ComponentsListNamespace] = UNSET,
    nevra: Union[Unset, None, str] = UNSET,
    nvr: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ofuri: Union[Unset, None, str] = UNSET,
    product_streams: Union[Unset, None, str] = UNSET,
    product_variants: Union[Unset, None, str] = UNSET,
    product_versions: Union[Unset, None, str] = UNSET,
    products: Union[Unset, None, str] = UNSET,
    provides: Union[Unset, None, str] = UNSET,
    purl: Union[Unset, None, str] = UNSET,
    re_name: Union[Unset, None, str] = UNSET,
    re_provides: Union[Unset, None, str] = UNSET,
    re_purl: Union[Unset, None, str] = UNSET,
    re_sources: Union[Unset, None, str] = UNSET,
    re_upstreams: Union[Unset, None, str] = UNSET,
    related_url: Union[Unset, None, str] = UNSET,
    release: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    sources: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, V1ComponentsListType] = UNSET,
    upstreams: Union[Unset, None, str] = UNSET,
    version: Union[Unset, None, str] = UNSET,
    view: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedComponentList]:
    """View for api/v1/components"""

    return sync_detailed(
        client=client,
        arch=arch,
        channels=channels,
        description=description,
        el_match=el_match,
        exclude_fields=exclude_fields,
        include_fields=include_fields,
        limit=limit,
        missing_copyright=missing_copyright,
        missing_license=missing_license,
        name=name,
        namespace=namespace,
        nevra=nevra,
        nvr=nvr,
        offset=offset,
        ofuri=ofuri,
        product_streams=product_streams,
        product_variants=product_variants,
        product_versions=product_versions,
        products=products,
        provides=provides,
        purl=purl,
        re_name=re_name,
        re_provides=re_provides,
        re_purl=re_purl,
        re_sources=re_sources,
        re_upstreams=re_upstreams,
        related_url=related_url,
        release=release,
        search=search,
        sources=sources,
        tags=tags,
        type=type,
        upstreams=upstreams,
        version=version,
        view=view,
    ).parsed
