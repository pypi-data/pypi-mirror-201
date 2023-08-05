from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="V1StatusListResponse200ResultsItemRelations")


@attr.s(auto_attribs=True)
class V1StatusListResponse200ResultsItemRelations(ComponentRegistryModel):
    """ """

    count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        count = d.pop("count", UNSET)

        v1_status_list_response_200_results_item_relations = cls(
            count=count,
        )

        v1_status_list_response_200_results_item_relations.additional_properties = d
        return v1_status_list_response_200_results_item_relations

    @staticmethod
    def get_fields():
        return {
            "count": int,
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
