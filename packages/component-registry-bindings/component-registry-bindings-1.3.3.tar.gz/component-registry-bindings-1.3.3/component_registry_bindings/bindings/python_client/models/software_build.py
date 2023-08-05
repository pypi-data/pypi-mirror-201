import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.build_type_enum import BuildTypeEnum
from ..models.software_build_components_item import SoftwareBuildComponentsItem
from ..models.tag import Tag
from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="SoftwareBuild")


@attr.s(auto_attribs=True)
class SoftwareBuild(ComponentRegistryModel):
    """Show detailed information for SoftwareBuild(s).
    Add or remove fields using ?include_fields=&exclude_fields="""

    link: str
    web_url: str
    build_id: int
    build_type: BuildTypeEnum
    name: str
    source: str
    tags: List[Tag]
    created_at: datetime.datetime
    last_changed: datetime.datetime
    components: List[SoftwareBuildComponentsItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        link = self.link
        web_url = self.web_url
        build_id = self.build_id
        build_type: str = UNSET
        if not isinstance(self.build_type, Unset):

            build_type = BuildTypeEnum(self.build_type).value

        name = self.name
        source = self.source
        tags: List[Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item: Dict[str, Any] = UNSET
                if not isinstance(tags_item_data, Unset):
                    tags_item = tags_item_data.to_dict()

                tags.append(tags_item)

        created_at: str = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        last_changed: str = UNSET
        if not isinstance(self.last_changed, Unset):
            last_changed = self.last_changed.isoformat()

        components: List[Dict[str, Any]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item: Dict[str, Any] = UNSET
                if not isinstance(components_item_data, Unset):
                    components_item = components_item_data.to_dict()

                components.append(components_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if link is not UNSET:
            field_dict["link"] = link
        if web_url is not UNSET:
            field_dict["web_url"] = web_url
        if build_id is not UNSET:
            field_dict["build_id"] = build_id
        if build_type is not UNSET:
            field_dict["build_type"] = build_type
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source
        if tags is not UNSET:
            field_dict["tags"] = tags
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if last_changed is not UNSET:
            field_dict["last_changed"] = last_changed
        if components is not UNSET:
            field_dict["components"] = components

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        link = d.pop("link", UNSET)

        web_url = d.pop("web_url", UNSET)

        build_id = d.pop("build_id", UNSET)

        _build_type = d.pop("build_type", UNSET)
        build_type: BuildTypeEnum
        if isinstance(_build_type, Unset):
            build_type = UNSET
        else:
            build_type = BuildTypeEnum(_build_type)

        name = d.pop("name", UNSET)

        source = d.pop("source", UNSET)

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

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _last_changed = d.pop("last_changed", UNSET)
        last_changed: datetime.datetime
        if isinstance(_last_changed, Unset):
            last_changed = UNSET
        else:
            last_changed = isoparse(_last_changed)

        components = []
        _components = d.pop("components", UNSET)
        if _components is UNSET:
            components = UNSET
        else:
            for components_item_data in _components or []:
                _components_item = components_item_data
                components_item: SoftwareBuildComponentsItem
                if isinstance(_components_item, Unset):
                    components_item = UNSET
                else:
                    components_item = SoftwareBuildComponentsItem.from_dict(
                        _components_item
                    )

                components.append(components_item)

        software_build = cls(
            link=link,
            web_url=web_url,
            build_id=build_id,
            build_type=build_type,
            name=name,
            source=source,
            tags=tags,
            created_at=created_at,
            last_changed=last_changed,
            components=components,
        )

        software_build.additional_properties = d
        return software_build

    @staticmethod
    def get_fields():
        return {
            "link": str,
            "web_url": str,
            "build_id": int,
            "build_type": BuildTypeEnum,
            "name": str,
            "source": str,
            "tags": List[Tag],
            "created_at": datetime.datetime,
            "last_changed": datetime.datetime,
            "components": List[SoftwareBuildComponentsItem],
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
