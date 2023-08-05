from enum import Enum


class V1ChannelsListType(str, Enum):
    CDN_REPO = "CDN_REPO"
    CONTAINER_REGISTRY = "CONTAINER_REGISTRY"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
