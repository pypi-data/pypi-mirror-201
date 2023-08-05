import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.channel_product_streams_item import ChannelProductStreamsItem
from ..models.channel_product_variants_item import ChannelProductVariantsItem
from ..models.channel_product_versions_item import ChannelProductVersionsItem
from ..models.channel_products_item import ChannelProductsItem
from ..models.channel_type_enum import ChannelTypeEnum
from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="Channel")


@attr.s(auto_attribs=True)
class Channel(ComponentRegistryModel):
    """Show detailed information for Channel(s).
    Add or remove fields using ?include_fields=&exclude_fields="""

    uuid: str
    link: str
    last_changed: datetime.datetime
    created_at: datetime.datetime
    name: str
    relative_url: str
    type: ChannelTypeEnum
    description: str
    products: List[ChannelProductsItem]
    product_versions: List[ChannelProductVersionsItem]
    product_streams: List[ChannelProductStreamsItem]
    product_variants: List[ChannelProductVariantsItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        link = self.link
        last_changed: str = UNSET
        if not isinstance(self.last_changed, Unset):
            last_changed = self.last_changed.isoformat()

        created_at: str = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        name = self.name
        relative_url = self.relative_url
        type: str = UNSET
        if not isinstance(self.type, Unset):

            type = ChannelTypeEnum(self.type).value

        description = self.description
        products: List[Dict[str, Any]] = UNSET
        if not isinstance(self.products, Unset):
            products = []
            for products_item_data in self.products:
                products_item: Dict[str, Any] = UNSET
                if not isinstance(products_item_data, Unset):
                    products_item = products_item_data.to_dict()

                products.append(products_item)

        product_versions: List[Dict[str, Any]] = UNSET
        if not isinstance(self.product_versions, Unset):
            product_versions = []
            for product_versions_item_data in self.product_versions:
                product_versions_item: Dict[str, Any] = UNSET
                if not isinstance(product_versions_item_data, Unset):
                    product_versions_item = product_versions_item_data.to_dict()

                product_versions.append(product_versions_item)

        product_streams: List[Dict[str, Any]] = UNSET
        if not isinstance(self.product_streams, Unset):
            product_streams = []
            for product_streams_item_data in self.product_streams:
                product_streams_item: Dict[str, Any] = UNSET
                if not isinstance(product_streams_item_data, Unset):
                    product_streams_item = product_streams_item_data.to_dict()

                product_streams.append(product_streams_item)

        product_variants: List[Dict[str, Any]] = UNSET
        if not isinstance(self.product_variants, Unset):
            product_variants = []
            for product_variants_item_data in self.product_variants:
                product_variants_item: Dict[str, Any] = UNSET
                if not isinstance(product_variants_item_data, Unset):
                    product_variants_item = product_variants_item_data.to_dict()

                product_variants.append(product_variants_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if link is not UNSET:
            field_dict["link"] = link
        if last_changed is not UNSET:
            field_dict["last_changed"] = last_changed
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if name is not UNSET:
            field_dict["name"] = name
        if relative_url is not UNSET:
            field_dict["relative_url"] = relative_url
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if products is not UNSET:
            field_dict["products"] = products
        if product_versions is not UNSET:
            field_dict["product_versions"] = product_versions
        if product_streams is not UNSET:
            field_dict["product_streams"] = product_streams
        if product_variants is not UNSET:
            field_dict["product_variants"] = product_variants

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        uuid = d.pop("uuid", UNSET)

        link = d.pop("link", UNSET)

        _last_changed = d.pop("last_changed", UNSET)
        last_changed: datetime.datetime
        if isinstance(_last_changed, Unset):
            last_changed = UNSET
        else:
            last_changed = isoparse(_last_changed)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        name = d.pop("name", UNSET)

        relative_url = d.pop("relative_url", UNSET)

        _type = d.pop("type", UNSET)
        type: ChannelTypeEnum
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ChannelTypeEnum(_type)

        description = d.pop("description", UNSET)

        products = []
        _products = d.pop("products", UNSET)
        if _products is UNSET:
            products = UNSET
        else:
            for products_item_data in _products or []:
                _products_item = products_item_data
                products_item: ChannelProductsItem
                if isinstance(_products_item, Unset):
                    products_item = UNSET
                else:
                    products_item = ChannelProductsItem.from_dict(_products_item)

                products.append(products_item)

        product_versions = []
        _product_versions = d.pop("product_versions", UNSET)
        if _product_versions is UNSET:
            product_versions = UNSET
        else:
            for product_versions_item_data in _product_versions or []:
                _product_versions_item = product_versions_item_data
                product_versions_item: ChannelProductVersionsItem
                if isinstance(_product_versions_item, Unset):
                    product_versions_item = UNSET
                else:
                    product_versions_item = ChannelProductVersionsItem.from_dict(
                        _product_versions_item
                    )

                product_versions.append(product_versions_item)

        product_streams = []
        _product_streams = d.pop("product_streams", UNSET)
        if _product_streams is UNSET:
            product_streams = UNSET
        else:
            for product_streams_item_data in _product_streams or []:
                _product_streams_item = product_streams_item_data
                product_streams_item: ChannelProductStreamsItem
                if isinstance(_product_streams_item, Unset):
                    product_streams_item = UNSET
                else:
                    product_streams_item = ChannelProductStreamsItem.from_dict(
                        _product_streams_item
                    )

                product_streams.append(product_streams_item)

        product_variants = []
        _product_variants = d.pop("product_variants", UNSET)
        if _product_variants is UNSET:
            product_variants = UNSET
        else:
            for product_variants_item_data in _product_variants or []:
                _product_variants_item = product_variants_item_data
                product_variants_item: ChannelProductVariantsItem
                if isinstance(_product_variants_item, Unset):
                    product_variants_item = UNSET
                else:
                    product_variants_item = ChannelProductVariantsItem.from_dict(
                        _product_variants_item
                    )

                product_variants.append(product_variants_item)

        channel = cls(
            uuid=uuid,
            link=link,
            last_changed=last_changed,
            created_at=created_at,
            name=name,
            relative_url=relative_url,
            type=type,
            description=description,
            products=products,
            product_versions=product_versions,
            product_streams=product_streams,
            product_variants=product_variants,
        )

        channel.additional_properties = d
        return channel

    @staticmethod
    def get_fields():
        return {
            "uuid": str,
            "link": str,
            "last_changed": datetime.datetime,
            "created_at": datetime.datetime,
            "name": str,
            "relative_url": str,
            "type": ChannelTypeEnum,
            "description": str,
            "products": List[ChannelProductsItem],
            "product_versions": List[ChannelProductVersionsItem],
            "product_streams": List[ChannelProductStreamsItem],
            "product_variants": List[ChannelProductVariantsItem],
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
