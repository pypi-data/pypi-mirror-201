from enum import Enum


class NamespaceEnum(str, Enum):
    UPSTREAM = "UPSTREAM"
    REDHAT = "REDHAT"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
