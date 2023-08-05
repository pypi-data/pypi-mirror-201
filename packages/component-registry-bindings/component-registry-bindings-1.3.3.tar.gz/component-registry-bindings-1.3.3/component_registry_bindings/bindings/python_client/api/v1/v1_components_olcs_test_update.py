from typing import Any, Dict, Optional

import requests

from ...client import Client
from ...models.component import Component
from ...types import UNSET, Response, Unset

QUERY_PARAMS = {}
REQUEST_BODY_TYPE = Component


def _get_kwargs(
    uuid: str,
    *,
    client: Client,
    form_data: Component,
    multipart_data: Component,
    json_body: Component,
) -> Dict[str, Any]:
    url = "{}/api/v1/components/{uuid}/olcs_test".format(
        client.base_url,
        uuid=uuid,
    )

    headers: Dict[str, Any] = client.get_headers()

    json_json_body: Dict[str, Any] = UNSET
    if not isinstance(json_body, Unset):
        json_body.to_dict()

    multipart_multipart_data: Dict[str, Any] = UNSET
    if not isinstance(multipart_data, Unset):
        multipart_data.to_multipart()

    return {
        "url": url,
        "headers": headers,
        "data": form_data.to_dict(),
    }


def _parse_response(*, response: requests.Response) -> Optional[Component]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: Component
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = Component.from_dict(_response_200)

        return response_200
    return None


def _build_response(*, response: requests.Response) -> Response[Component]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: Client,
    form_data: Component,
    multipart_data: Component,
    json_body: Component,
) -> Response[Component]:
    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    )

    response = requests.put(
        verify=client.verify_ssl,
        auth=client.auth,
        timeout=client.timeout,
        **kwargs,
    )
    response.raise_for_status()

    return _build_response(response=response)


def sync(
    uuid: str,
    *,
    client: Client,
    form_data: Component,
    multipart_data: Component,
    json_body: Component,
) -> Optional[Component]:
    """Allow OpenLCS to upload copyright text / license scan results for a component"""

    return sync_detailed(
        uuid=uuid,
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    ).parsed
