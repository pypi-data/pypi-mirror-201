from typing import Any, Dict, List, Type, TypeVar

import attr

from ..types import ComponentRegistryModel

T = TypeVar("T", bound="ProductVersionProductStreamsItem")


@attr.s(auto_attribs=True)
class ProductVersionProductStreamsItem(ComponentRegistryModel):
    """ """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        product_version_product_streams_item = cls()

        product_version_product_streams_item.additional_properties = d
        return product_version_product_streams_item

    @staticmethod
    def get_fields():
        return {}

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
