from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.product_variant_channels_item import ProductVariantChannelsItem
from ..models.product_variant_product_streams_item import (
    ProductVariantProductStreamsItem,
)
from ..models.product_variant_product_versions_item import (
    ProductVariantProductVersionsItem,
)
from ..models.product_variant_products_item import ProductVariantProductsItem
from ..models.product_variant_relations_item import ProductVariantRelationsItem
from ..models.tag import Tag
from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="ProductVariant")


@attr.s(auto_attribs=True)
class ProductVariant(ComponentRegistryModel):
    """Show detailed information for ProductVariant(s).
    Add or remove fields using ?include_fields=&exclude_fields="""

    link: str
    uuid: str
    ofuri: str
    name: str
    description: str
    build_count: int
    builds: str
    components: str
    upstreams: str
    tags: List[Tag]
    channels: List[ProductVariantChannelsItem]
    relations: List[ProductVariantRelationsItem]
    products: List[ProductVariantProductsItem]
    product_versions: List[ProductVariantProductVersionsItem]
    product_streams: List[ProductVariantProductStreamsItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        link = self.link
        uuid = self.uuid
        ofuri = self.ofuri
        name = self.name
        description = self.description
        build_count = self.build_count
        builds = self.builds
        components = self.components
        upstreams = self.upstreams
        tags: List[Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item: Dict[str, Any] = UNSET
                if not isinstance(tags_item_data, Unset):
                    tags_item = tags_item_data.to_dict()

                tags.append(tags_item)

        channels: List[Dict[str, Any]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = []
            for channels_item_data in self.channels:
                channels_item: Dict[str, Any] = UNSET
                if not isinstance(channels_item_data, Unset):
                    channels_item = channels_item_data.to_dict()

                channels.append(channels_item)

        relations: List[Dict[str, Any]] = UNSET
        if not isinstance(self.relations, Unset):
            relations = []
            for relations_item_data in self.relations:
                relations_item: Dict[str, Any] = UNSET
                if not isinstance(relations_item_data, Unset):
                    relations_item = relations_item_data.to_dict()

                relations.append(relations_item)

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if link is not UNSET:
            field_dict["link"] = link
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if ofuri is not UNSET:
            field_dict["ofuri"] = ofuri
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if build_count is not UNSET:
            field_dict["build_count"] = build_count
        if builds is not UNSET:
            field_dict["builds"] = builds
        if components is not UNSET:
            field_dict["components"] = components
        if upstreams is not UNSET:
            field_dict["upstreams"] = upstreams
        if tags is not UNSET:
            field_dict["tags"] = tags
        if channels is not UNSET:
            field_dict["channels"] = channels
        if relations is not UNSET:
            field_dict["relations"] = relations
        if products is not UNSET:
            field_dict["products"] = products
        if product_versions is not UNSET:
            field_dict["product_versions"] = product_versions
        if product_streams is not UNSET:
            field_dict["product_streams"] = product_streams

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        link = d.pop("link", UNSET)

        uuid = d.pop("uuid", UNSET)

        ofuri = d.pop("ofuri", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        build_count = d.pop("build_count", UNSET)

        builds = d.pop("builds", UNSET)

        components = d.pop("components", UNSET)

        upstreams = d.pop("upstreams", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        if _tags is UNSET:
            tags = UNSET
        else:
            for tags_item_data in _tags or []:
                _tags_item = tags_item_data
                tags_item: Tag
                if isinstance(_tags_item, Unset):
                    tags_item = UNSET
                else:
                    tags_item = Tag.from_dict(_tags_item)

                tags.append(tags_item)

        channels = []
        _channels = d.pop("channels", UNSET)
        if _channels is UNSET:
            channels = UNSET
        else:
            for channels_item_data in _channels or []:
                _channels_item = channels_item_data
                channels_item: ProductVariantChannelsItem
                if isinstance(_channels_item, Unset):
                    channels_item = UNSET
                else:
                    channels_item = ProductVariantChannelsItem.from_dict(_channels_item)

                channels.append(channels_item)

        relations = []
        _relations = d.pop("relations", UNSET)
        if _relations is UNSET:
            relations = UNSET
        else:
            for relations_item_data in _relations or []:
                _relations_item = relations_item_data
                relations_item: ProductVariantRelationsItem
                if isinstance(_relations_item, Unset):
                    relations_item = UNSET
                else:
                    relations_item = ProductVariantRelationsItem.from_dict(
                        _relations_item
                    )

                relations.append(relations_item)

        products = []
        _products = d.pop("products", UNSET)
        if _products is UNSET:
            products = UNSET
        else:
            for products_item_data in _products or []:
                _products_item = products_item_data
                products_item: ProductVariantProductsItem
                if isinstance(_products_item, Unset):
                    products_item = UNSET
                else:
                    products_item = ProductVariantProductsItem.from_dict(_products_item)

                products.append(products_item)

        product_versions = []
        _product_versions = d.pop("product_versions", UNSET)
        if _product_versions is UNSET:
            product_versions = UNSET
        else:
            for product_versions_item_data in _product_versions or []:
                _product_versions_item = product_versions_item_data
                product_versions_item: ProductVariantProductVersionsItem
                if isinstance(_product_versions_item, Unset):
                    product_versions_item = UNSET
                else:
                    product_versions_item = ProductVariantProductVersionsItem.from_dict(
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
                product_streams_item: ProductVariantProductStreamsItem
                if isinstance(_product_streams_item, Unset):
                    product_streams_item = UNSET
                else:
                    product_streams_item = ProductVariantProductStreamsItem.from_dict(
                        _product_streams_item
                    )

                product_streams.append(product_streams_item)

        product_variant = cls(
            link=link,
            uuid=uuid,
            ofuri=ofuri,
            name=name,
            description=description,
            build_count=build_count,
            builds=builds,
            components=components,
            upstreams=upstreams,
            tags=tags,
            channels=channels,
            relations=relations,
            products=products,
            product_versions=product_versions,
            product_streams=product_streams,
        )

        product_variant.additional_properties = d
        return product_variant

    @staticmethod
    def get_fields():
        return {
            "link": str,
            "uuid": str,
            "ofuri": str,
            "name": str,
            "description": str,
            "build_count": int,
            "builds": str,
            "components": str,
            "upstreams": str,
            "tags": List[Tag],
            "channels": List[ProductVariantChannelsItem],
            "relations": List[ProductVariantRelationsItem],
            "products": List[ProductVariantProductsItem],
            "product_versions": List[ProductVariantProductVersionsItem],
            "product_streams": List[ProductVariantProductStreamsItem],
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
