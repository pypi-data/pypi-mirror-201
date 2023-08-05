from typing import Any, Dict, Optional, Union

import requests

from ...client import AuthenticatedClient
from ...models.v1_schema_retrieve_format import V1SchemaRetrieveFormat
from ...models.v1_schema_retrieve_response_200 import V1SchemaRetrieveResponse200
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {
    "format": V1SchemaRetrieveFormat,
}


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, V1SchemaRetrieveFormat] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/schema".format(
        client.base_url,
    )

    headers: Dict[str, Any] = client.get_headers()

    json_format_: Union[Unset, None, str] = UNSET
    if not isinstance(format_, Unset):

        json_format_ = V1SchemaRetrieveFormat(format_).value if format_ else None

    params: Dict[str, Any] = {
        "format": json_format_,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "params": params,
    }


def _parse_response(
    *, response: requests.Response
) -> Optional[V1SchemaRetrieveResponse200]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: V1SchemaRetrieveResponse200
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = V1SchemaRetrieveResponse200.from_dict(_response_200)

        return response_200
    return None


def _build_response(
    *, response: requests.Response
) -> Response[V1SchemaRetrieveResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, V1SchemaRetrieveFormat] = UNSET,
) -> Response[V1SchemaRetrieveResponse200]:
    kwargs = _get_kwargs(
        client=client,
        format_=format_,
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
    client: AuthenticatedClient,
    format_: Union[Unset, None, V1SchemaRetrieveFormat] = UNSET,
) -> Optional[V1SchemaRetrieveResponse200]:
    """OpenApi3 schema for this API. Format can be selected via content negotiation.

    - YAML: application/vnd.oai.openapi
    - JSON: application/vnd.oai.openapi+json"""

    return sync_detailed(
        client=client,
        format_=format_,
    ).parsed
