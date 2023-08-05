from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.build_type_enum import BuildTypeEnum
from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="SoftwareBuildSummary")


@attr.s(auto_attribs=True)
class SoftwareBuildSummary(ComponentRegistryModel):
    """Show summary information for a SoftwareBuild.
    Add or remove fields using ?include_fields=&exclude_fields="""

    link: str
    build_id: int
    build_type: BuildTypeEnum
    name: str
    source: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        link = self.link
        build_id = self.build_id
        build_type: str = UNSET
        if not isinstance(self.build_type, Unset):

            build_type = BuildTypeEnum(self.build_type).value

        name = self.name
        source = self.source

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if link is not UNSET:
            field_dict["link"] = link
        if build_id is not UNSET:
            field_dict["build_id"] = build_id
        if build_type is not UNSET:
            field_dict["build_type"] = build_type
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        link = d.pop("link", UNSET)

        build_id = d.pop("build_id", UNSET)

        _build_type = d.pop("build_type", UNSET)
        build_type: BuildTypeEnum
        if isinstance(_build_type, Unset):
            build_type = UNSET
        else:
            build_type = BuildTypeEnum(_build_type)

        name = d.pop("name", UNSET)

        source = d.pop("source", UNSET)

        software_build_summary = cls(
            link=link,
            build_id=build_id,
            build_type=build_type,
            name=name,
            source=source,
        )

        software_build_summary.additional_properties = d
        return software_build_summary

    @staticmethod
    def get_fields():
        return {
            "link": str,
            "build_id": int,
            "build_type": BuildTypeEnum,
            "name": str,
            "source": str,
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
