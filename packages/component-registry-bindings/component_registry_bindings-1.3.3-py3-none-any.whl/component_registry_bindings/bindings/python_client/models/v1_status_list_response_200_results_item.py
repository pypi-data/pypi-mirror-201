import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.v1_status_list_response_200_results_item_builds import (
    V1StatusListResponse200ResultsItemBuilds,
)
from ..models.v1_status_list_response_200_results_item_channels import (
    V1StatusListResponse200ResultsItemChannels,
)
from ..models.v1_status_list_response_200_results_item_components import (
    V1StatusListResponse200ResultsItemComponents,
)
from ..models.v1_status_list_response_200_results_item_product_streams import (
    V1StatusListResponse200ResultsItemProductStreams,
)
from ..models.v1_status_list_response_200_results_item_product_variants import (
    V1StatusListResponse200ResultsItemProductVariants,
)
from ..models.v1_status_list_response_200_results_item_product_versions import (
    V1StatusListResponse200ResultsItemProductVersions,
)
from ..models.v1_status_list_response_200_results_item_products import (
    V1StatusListResponse200ResultsItemProducts,
)
from ..models.v1_status_list_response_200_results_item_relations import (
    V1StatusListResponse200ResultsItemRelations,
)
from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="V1StatusListResponse200ResultsItem")


@attr.s(auto_attribs=True)
class V1StatusListResponse200ResultsItem(ComponentRegistryModel):
    """ """

    status: Union[Unset, str] = UNSET
    dt: Union[Unset, datetime.datetime] = UNSET
    service_version: Union[Unset, str] = UNSET
    rest_api_version: Union[Unset, str] = UNSET
    db_size: Union[Unset, str] = UNSET
    builds: Union[Unset, V1StatusListResponse200ResultsItemBuilds] = UNSET
    products: Union[Unset, V1StatusListResponse200ResultsItemProducts] = UNSET
    product_versions: Union[
        Unset, V1StatusListResponse200ResultsItemProductVersions
    ] = UNSET
    product_streams: Union[
        Unset, V1StatusListResponse200ResultsItemProductStreams
    ] = UNSET
    product_variants: Union[
        Unset, V1StatusListResponse200ResultsItemProductVariants
    ] = UNSET
    channels: Union[Unset, V1StatusListResponse200ResultsItemChannels] = UNSET
    components: Union[Unset, V1StatusListResponse200ResultsItemComponents] = UNSET
    relations: Union[Unset, V1StatusListResponse200ResultsItemRelations] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        dt: Union[Unset, str] = UNSET
        if not isinstance(self.dt, Unset):
            dt = self.dt.isoformat()

        service_version = self.service_version
        rest_api_version = self.rest_api_version
        db_size = self.db_size
        builds: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.builds, Unset):
            builds = self.builds.to_dict()

        products: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.products, Unset):
            products = self.products.to_dict()

        product_versions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product_versions, Unset):
            product_versions = self.product_versions.to_dict()

        product_streams: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product_streams, Unset):
            product_streams = self.product_streams.to_dict()

        product_variants: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product_variants, Unset):
            product_variants = self.product_variants.to_dict()

        channels: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = self.channels.to_dict()

        components: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.components, Unset):
            components = self.components.to_dict()

        relations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relations, Unset):
            relations = self.relations.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if status is not UNSET:
            field_dict["status"] = status
        if dt is not UNSET:
            field_dict["dt"] = dt
        if service_version is not UNSET:
            field_dict["service_version"] = service_version
        if rest_api_version is not UNSET:
            field_dict["rest_api_version"] = rest_api_version
        if db_size is not UNSET:
            field_dict["db_size"] = db_size
        if builds is not UNSET:
            field_dict["builds"] = builds
        if products is not UNSET:
            field_dict["products"] = products
        if product_versions is not UNSET:
            field_dict["product_versions"] = product_versions
        if product_streams is not UNSET:
            field_dict["product_streams"] = product_streams
        if product_variants is not UNSET:
            field_dict["product_variants"] = product_variants
        if channels is not UNSET:
            field_dict["channels"] = channels
        if components is not UNSET:
            field_dict["components"] = components
        if relations is not UNSET:
            field_dict["relations"] = relations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        status = d.pop("status", UNSET)

        _dt = d.pop("dt", UNSET)
        dt: Union[Unset, datetime.datetime]
        if isinstance(_dt, Unset):
            dt = UNSET
        else:
            dt = isoparse(_dt)

        service_version = d.pop("service_version", UNSET)

        rest_api_version = d.pop("rest_api_version", UNSET)

        db_size = d.pop("db_size", UNSET)

        _builds = d.pop("builds", UNSET)
        builds: Union[Unset, V1StatusListResponse200ResultsItemBuilds]
        if isinstance(_builds, Unset):
            builds = UNSET
        else:
            builds = V1StatusListResponse200ResultsItemBuilds.from_dict(_builds)

        _products = d.pop("products", UNSET)
        products: Union[Unset, V1StatusListResponse200ResultsItemProducts]
        if isinstance(_products, Unset):
            products = UNSET
        else:
            products = V1StatusListResponse200ResultsItemProducts.from_dict(_products)

        _product_versions = d.pop("product_versions", UNSET)
        product_versions: Union[
            Unset, V1StatusListResponse200ResultsItemProductVersions
        ]
        if isinstance(_product_versions, Unset):
            product_versions = UNSET
        else:
            product_versions = (
                V1StatusListResponse200ResultsItemProductVersions.from_dict(
                    _product_versions
                )
            )

        _product_streams = d.pop("product_streams", UNSET)
        product_streams: Union[Unset, V1StatusListResponse200ResultsItemProductStreams]
        if isinstance(_product_streams, Unset):
            product_streams = UNSET
        else:
            product_streams = (
                V1StatusListResponse200ResultsItemProductStreams.from_dict(
                    _product_streams
                )
            )

        _product_variants = d.pop("product_variants", UNSET)
        product_variants: Union[
            Unset, V1StatusListResponse200ResultsItemProductVariants
        ]
        if isinstance(_product_variants, Unset):
            product_variants = UNSET
        else:
            product_variants = (
                V1StatusListResponse200ResultsItemProductVariants.from_dict(
                    _product_variants
                )
            )

        _channels = d.pop("channels", UNSET)
        channels: Union[Unset, V1StatusListResponse200ResultsItemChannels]
        if isinstance(_channels, Unset):
            channels = UNSET
        else:
            channels = V1StatusListResponse200ResultsItemChannels.from_dict(_channels)

        _components = d.pop("components", UNSET)
        components: Union[Unset, V1StatusListResponse200ResultsItemComponents]
        if isinstance(_components, Unset):
            components = UNSET
        else:
            components = V1StatusListResponse200ResultsItemComponents.from_dict(
                _components
            )

        _relations = d.pop("relations", UNSET)
        relations: Union[Unset, V1StatusListResponse200ResultsItemRelations]
        if isinstance(_relations, Unset):
            relations = UNSET
        else:
            relations = V1StatusListResponse200ResultsItemRelations.from_dict(
                _relations
            )

        v1_status_list_response_200_results_item = cls(
            status=status,
            dt=dt,
            service_version=service_version,
            rest_api_version=rest_api_version,
            db_size=db_size,
            builds=builds,
            products=products,
            product_versions=product_versions,
            product_streams=product_streams,
            product_variants=product_variants,
            channels=channels,
            components=components,
            relations=relations,
        )

        v1_status_list_response_200_results_item.additional_properties = d
        return v1_status_list_response_200_results_item

    @staticmethod
    def get_fields():
        return {
            "status": str,
            "dt": datetime.datetime,
            "service_version": str,
            "rest_api_version": str,
            "db_size": str,
            "builds": V1StatusListResponse200ResultsItemBuilds,
            "products": V1StatusListResponse200ResultsItemProducts,
            "product_versions": V1StatusListResponse200ResultsItemProductVersions,
            "product_streams": V1StatusListResponse200ResultsItemProductStreams,
            "product_variants": V1StatusListResponse200ResultsItemProductVariants,
            "channels": V1StatusListResponse200ResultsItemChannels,
            "components": V1StatusListResponse200ResultsItemComponents,
            "relations": V1StatusListResponse200ResultsItemRelations,
        }

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
