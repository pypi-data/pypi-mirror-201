from typing import Dict, List

COMPONENT_REGISTRY_API_VERSION: str = "v1"
COMPONENT_REGISTRY_BINDINGS_USERAGENT: str = "component-registry-bindings-1.3.3"
COMPONENT_REGISTRY_BINDINGS_API_PATH: str = (
    f".bindings.python_client.api.{COMPONENT_REGISTRY_API_VERSION}"
)

# all available session operations
ALL_SESSION_OPERATIONS: List[str] = (
    "retrieve",
    "update",
    "list",
    "create",
    "destroy",
    "search",
)

# mapping for resources which model names are different from the endpoint name
RESOURCE_TO_MODEL_MAPPING: Dict[str, str] = {
    "builds": "SoftwareBuild",
}
