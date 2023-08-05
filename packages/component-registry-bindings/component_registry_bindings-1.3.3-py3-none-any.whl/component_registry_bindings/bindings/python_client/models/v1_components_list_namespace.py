from enum import Enum


class V1ComponentsListNamespace(str, Enum):
    REDHAT = "REDHAT"
    UPSTREAM = "UPSTREAM"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
