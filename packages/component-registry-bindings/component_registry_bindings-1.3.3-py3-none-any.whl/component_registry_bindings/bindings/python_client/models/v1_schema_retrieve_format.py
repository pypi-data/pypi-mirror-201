from enum import Enum


class V1SchemaRetrieveFormat(str, Enum):
    JSON = "json"
    YAML = "yaml"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
