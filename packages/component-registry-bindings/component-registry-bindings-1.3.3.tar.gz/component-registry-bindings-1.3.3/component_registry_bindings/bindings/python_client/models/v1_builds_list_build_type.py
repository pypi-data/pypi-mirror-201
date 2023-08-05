from enum import Enum


class V1BuildsListBuildType(str, Enum):
    BREW = "BREW"
    KOJI = "KOJI"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
