import importlib
import re
from functools import partial
from types import ModuleType
from typing import Any, Callable, Dict, List, Union

from .bindings.python_client import AuthenticatedClient, models
from .bindings.python_client.types import UNSET
from .constants import (
    ALL_SESSION_OPERATIONS,
    COMPONENT_REGISTRY_API_VERSION,
    COMPONENT_REGISTRY_BINDINGS_API_PATH,
    COMPONENT_REGISTRY_BINDINGS_USERAGENT,
    RESOURCE_TO_MODEL_MAPPING,
)

component_registry_status_retrieve = importlib.import_module(
    f"{COMPONENT_REGISTRY_BINDINGS_API_PATH}.{COMPONENT_REGISTRY_API_VERSION}_status_list",
    package="component_registry_bindings",
)


class OperationUnsupported(Exception):
    """Session operation is unsupported exception"""


def get_sync_function(api_module: ModuleType) -> Callable:
    """
    Get 'sync' function from API module if available (response example is defined in schema)
    or get basic 'sync_detailed' function (response example is not defined in schema)
    """
    return getattr(api_module, "sync", getattr(api_module, "sync_detailed"))


def new_session(
    component_registry_server_uri: str, verify_ssl: Union[str, bool] = True
):
    """Create a new session for selected Component Registry URI"""

    # strip trailing slash
    if component_registry_server_uri.endswith("/"):
        component_registry_server_uri = component_registry_server_uri[:-1]

    return Session(base_url=component_registry_server_uri, verify_ssl=verify_ssl)


class Session:
    """Simple session wrapper which encapsulates the client"""

    def __init__(self, base_url: str, verify_ssl: Union[str, bool] = True):

        self.__client = AuthenticatedClient(
            base_url=base_url,
            headers={"User-Agent": COMPONENT_REGISTRY_BINDINGS_USERAGENT},
            verify_ssl=verify_ssl,
        )

        self.builds = SessionOperationsGroup(
            self.__client,
            "builds",
            allowed_operations=("retrieve", "list"),
        )
        self.components = SessionOperationsGroup(
            self.__client,
            "components",
            allowed_operations=("retrieve", "list"),
        )
        self.products = SessionOperationsGroup(
            self.__client,
            "products",
            allowed_operations=("retrieve", "list"),
        )
        self.product_versions = SessionOperationsGroup(
            self.__client,
            "product_versions",
            allowed_operations=("retrieve", "list"),
        )
        self.product_streams = SessionOperationsGroup(
            self.__client,
            "product_streams",
            allowed_operations=("retrieve", "list"),
        )
        self.product_variants = SessionOperationsGroup(
            self.__client,
            "product_variants",
            allowed_operations=("retrieve", "list"),
        )
        self.channels = SessionOperationsGroup(
            self.__client, "channels", allowed_operations=("retrieve", "list")
        )

    def status(self):
        status_fn = get_sync_function(component_registry_status_retrieve)
        return status_fn(client=self.__client)


class SessionOperationsGroup:
    """
    Group of the CRUD and extra operations for one specific resource
    """

    def __init__(
        self,
        client: AuthenticatedClient,
        resource_name: str,
        allowed_operations: List[str] = ALL_SESSION_OPERATIONS,
    ):
        self.client = client
        self.resource_name = resource_name
        self.allowed_operations = allowed_operations

    @property
    def model_name(self) -> str:
        if self.resource_name in RESOURCE_TO_MODEL_MAPPING:
            # from mapping
            return RESOURCE_TO_MODEL_MAPPING[self.resource_name]
        else:
            # parse it from the resource name
            name_components = self.resource_name.split("_")
            name_components[-1] = name_components[-1][:-1]
            return "".join(name_component.title() for name_component in name_components)

    @property
    def model(self):
        return getattr(models, self.model_name)

    def __get_method_module(self, resource_name: str, method: str) -> ModuleType:
        # import endpoint module based on a method
        return importlib.import_module(
            f"{COMPONENT_REGISTRY_BINDINGS_API_PATH}.{COMPONENT_REGISTRY_API_VERSION}_{resource_name}_{method}",
            package="component_registry_bindings",
        )

    def __make_iterable(self, response, **kwargs):
        """
        Populate next, prev and iterator helper methods for paginated responses
        """

        response.iterator = Paginator(
            session_operation=self.retrieve_list, init_response=response
        )

        for param_name, func_name in (("next_", "next"), ("previous", "prev")):
            kwargs.pop("limit", None)
            kwargs.pop("offset", None)
            param = getattr(response, param_name, None)
            if param in (None, UNSET):
                setattr(response, func_name, lambda: None)
            else:
                limit = re.search("limit=(\d+)", param)
                if limit is not None:
                    kwargs["limit"] = limit.group(1)
                offset = re.search("offset=(\d+)", param)
                if offset is not None:
                    kwargs["offset"] = offset.group(1)

                setattr(response, func_name, partial(self.retrieve_list, **kwargs))

        return response

    # CRUD operations

    def retrieve(self, id, **kwargs):
        if "retrieve" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            raise OperationUnsupported(
                'Operation "retrieve" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def retrieve_list(self, **kwargs):
        if "list" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="list"
            )
            sync_fn = get_sync_function(method_module)
            return self.__make_iterable(sync_fn(client=self.client, **kwargs), **kwargs)
        else:
            raise OperationUnsupported(
                'Operation "retrieve_list" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def create(self, form_data: Dict[str, Any]):
        if "create" in self.allowed_operations:
            transformed_data = self.model.from_dict(form_data)

            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="create"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(
                client=self.client,
                form_data=transformed_data,
                multipart_data=UNSET,
                json_body=UNSET,
            )
        else:
            raise OperationUnsupported(
                'Operation "create" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def update(self, id, form_data: Dict[str, Any]):
        if "update" in self.allowed_operations:
            transformed_data = self.model.from_dict(form_data)

            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="update"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(
                id,
                client=self.client,
                form_data=transformed_data,
                multipart_data=UNSET,
                json_body=UNSET,
            )
        else:
            raise OperationUnsupported(
                'Operation "update" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def delete(self, id):
        if "destroy" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="destroy"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(
                id,
                client=self.client,
            )
        else:
            raise OperationUnsupported(
                'Operation "delete" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    # Extra operations

    def search(self, searched_text: str):
        if "search" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="list"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(client=self.client, search=searched_text)
        else:
            raise OperationUnsupported(
                'Operation "search" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def retrieve_provides(self, id, **kwargs):
        # TODO: Once the schema in Component Registry is adjusted, allow this for the
        # particular resources
        if "retrieve_provides" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="provides_retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            raise OperationUnsupported(
                'Operation "retrieve_provides" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def retrieve_taxonomy(self, id, **kwargs):
        # TODO: Once the schema in Component Registry is adjusted, allow this for the
        # particular resources
        if "retrieve" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="taxonomy_retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            raise OperationUnsupported(
                'Operation "retrieve_taxonomy" is not supported for the '
                f'"{self.resource_name}" resource.'
            )

    def retrieve_manifest(self, id, **kwargs):
        # TODO: Once the schema in Component Registry is adjusted, allow this for the
        # particular resources
        if "retrieve" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="manifest_retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            raise OperationUnsupported(
                'Operation "retrieve_manifest" is not supported for the '
                f'"{self.resource_name}" resource.'
            )


class Paginator:
    """
    Iterable for handling API pagination.

    Receives either starting limit and offset or already existing response from which
    it should continue.

    It keeps calling `.next()` response until pages are exhausted.
    """

    def __init__(
        self,
        session_operation: Callable,
        limit: int = 100,
        offset: int = 0,
        init_response=None,
        **kwargs,
    ):
        self.session_operation = session_operation
        self.__init_limit = limit
        self.__init_offset = offset
        self.__init_response = init_response
        self.current_response = init_response
        self.kwargs = kwargs

    def __iter__(self):
        self.current_response = self.__init_response
        return self

    def __next__(self):
        if self.current_response is None:
            response = self.session_operation(
                limit=self.__init_limit, offset=self.__init_offset, **self.kwargs
            )
            self.current_response = response
            return response
        else:
            response = self.current_response.next()
            if response is not None:
                self.current_response = response
                return response
            else:
                raise StopIteration
