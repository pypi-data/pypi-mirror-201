from enum import Enum


class V1ComponentsListType(str, Enum):
    CARGO = "CARGO"
    GEM = "GEM"
    GENERIC = "GENERIC"
    GITHUB = "GITHUB"
    GOLANG = "GOLANG"
    MAVEN = "MAVEN"
    NPM = "NPM"
    OCI = "OCI"
    PYPI = "PYPI"
    RPM = "RPM"
    RPMMOD = "RPMMOD"
    # This is a temporary tweak to accept empty Enum
    NONE = ""

    def __str__(self) -> str:
        return str(self.value)
