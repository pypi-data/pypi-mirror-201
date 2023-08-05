import asyncio
import enum
import os
import datetime
import logging

from dataclasses import dataclass

from typing import List, Any, Optional, Type

from packaging import version as packaging_version, specifiers

from graphql_api.remote import GraphQLRemoteObject, GraphQLRemoteExecutor
from graphql_api.utils import to_camel_case

from graphql_api import GraphQLAPI, field

from graphql_http_server import GraphQLHTTPServer


class ServiceConnectionState(enum.Enum):
    UNKNOWN = "UNKNOWN"
    CONFIG_ERROR = "CONFIG_ERROR"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    OK = "OK"


@dataclass
class ServiceConnection:
    name: str
    api_version_specifier: Optional[str] = None
    api_url: str = None
    service_manager_url: Optional[str] = None
    http_method: str = "POST"
    raise_error: bool = True
    schema: Type = None
    state: ServiceConnectionState = ServiceConnectionState.UNKNOWN

    remote_name: Optional[str] = None
    remote_api_version: Optional[str] = None
    remote_service_manager: 'ServiceManager' = None
    remote_service_manager_api: GraphQLRemoteObject = None

    @classmethod
    def graphql_exclude_fields(cls) -> List[str]:
        return ['schema', 'remote_service', 'remote_service_api']

    def __post_init__(self):
        if self.schema:
            if hasattr(self.schema, "api_version"):
                try:
                    schema_api_version = getattr(self.schema, "api_version")
                    schema_api_version = packaging_version.Version(
                        schema_api_version
                    )
                    if not self.api_version_specifier:
                        self.api_version_specifier = \
                            f"~={schema_api_version.major}" \
                            f".{schema_api_version.minor}"
                except Exception:
                    logging.warning(
                        f"Could not identify the api_version for the "
                        f"connection to {self.name} at {self.api_url}"
                    )

        if self.api_url and self.schema:
            self.remote_service_manager_api = GraphQLRemoteObject(
                executor=GraphQLRemoteExecutor(
                    name=to_camel_case(self.name, title=True),
                    url=self.api_url,
                    http_method=self.http_method
                ),
                api=GraphQLAPI(root=self.schema)
            )

    async def async_connect(
            self,
            logs: List = None,
            timeout: int = 5
    ) -> bool:

        if logs is None:
            logs = []

        if not self.api_url:
            self.state = ServiceConnectionState.CONFIG_ERROR
            logs.append(f"[{datetime.datetime.utcnow()}] ERROR: Missing URL"
                        f" for service {self.name}")

            if self.raise_error:
                raise TypeError(f"Missing URL for service {self.name}")
            return False

        if not self.schema:
            self.state = ServiceConnectionState.CONFIG_ERROR
            logs.append(f"[{datetime.datetime.utcnow()}] ERROR: Missing schema"
                        f" for service {self.name}")

            if self.raise_error:
                raise TypeError(f"Missing schema for service {self.name}")
            return False

        name = to_camel_case(self.name, title=True) + "Service"

        logs.append(
            f"[{datetime.datetime.utcnow()}] "
            f"connecting to {name} {self.api_url}"
        )

        if self.service_manager_url:

            # Attempt to connect to a Service Directory
            logs.append(
                f"[{datetime.datetime.utcnow()}]  Connecting to Service "
                f"Manager for {name} {self.service_manager_url}"
            )

            # noinspection PyTypeChecker
            self.remote_service_manager: ServiceManager = GraphQLRemoteObject(
                executor=GraphQLRemoteExecutor(
                    name=name,
                    url=self.service_manager_url,
                    http_method=self.http_method,
                    http_timeout=timeout
                ),
                api=GraphQLAPI(root=ServiceManager)
            )

            a = datetime.datetime.now()

            try:
                uptime = await self.remote_service_manager.call_async("uptime")
            except Exception as err:
                logs.append(
                    f"[{datetime.datetime.utcnow()}] ERROR: Unable to connect "
                    f"to {name}, timed out after "
                    f"{timeout} seconds, error {err}"
                )
                self.state = ServiceConnectionState.CONNECTION_ERROR

                if self.raise_error:
                    raise ConnectionError(
                        f"Unable to connect to {name}, timed out after "
                        f"{timeout} seconds, error {err}"
                    )
                return False

            b = datetime.datetime.now()

            self.remote_name = await self.remote_service_manager \
                .call_async("name")
            self.remote_api_version = await \
                self.remote_service_manager.call_async("api_version")

            delta = b - a
            logs.append(f"[{datetime.datetime.utcnow()}] {name} "
                        f"Response time {delta} Uptime {uptime}")

            if self.api_version_specifier:
                try:
                    specifier = specifiers.Specifier(
                        self.api_version_specifier
                    )
                except specifiers.InvalidSpecifier as err:
                    logs.append(
                        f"[{datetime.datetime.utcnow()}] "
                        f"ERROR: {name} malformed api version specifier "
                        f"{self.api_version_specifier}"
                    )
                    self.state = ServiceConnectionState.VALIDATION_ERROR
                    if self.raise_error:
                        raise err
                    return False

                try:
                    service_version = packaging_version.Version(
                        self.remote_api_version
                    )
                except packaging_version.InvalidVersion as err:
                    logs.append(
                        f"[{datetime.datetime.utcnow()}] "
                        f"ERROR: {name} malformed api version found "
                        f"{self.remote_api_version}"
                    )
                    self.state = ServiceConnectionState.VALIDATION_ERROR
                    if self.raise_error:
                        raise err
                    return False

                if not specifier.contains(service_version):
                    logs.append(
                        f"[{datetime.datetime.utcnow()}] ERROR: Api version "
                        f"mismatch, found {self.remote_api_version}, "
                        f"required {self.api_version_specifier}"
                    )
                    self.state = ServiceConnectionState.VALIDATION_ERROR
                    if self.raise_error:
                        raise TypeError(
                            f"[{datetime.datetime.utcnow()}] {name} api "
                            f"version mismatch at {self.api_url}, expecting "
                            f"version {self.api_version_specifier} but "
                            f"{self.api_url} identified as {self.remote_name} "
                            f"version {self.remote_api_version}."
                        )
                    return False
                else:
                    logs.append(
                        f"[{datetime.datetime.utcnow()}] {name} api version "
                        f"match {self.remote_api_version} is valid for "
                        f"{self.api_version_specifier}"
                    )

        executor = GraphQLRemoteExecutor(
            name=name,
            url=self.api_url,
            http_method=self.http_method,
            http_timeout=timeout
        )

        try:
            response = await executor.execute_async("query { __typename }")
        except Exception as err:
            logs.append(
                f"[{datetime.datetime.utcnow()}] ERROR: {name} API error "
                f"from {self.api_url}, {err}"
            )
            self.state = ServiceConnectionState.CONNECTION_ERROR
            if self.raise_error:
                raise err
            return False
        else:
            if response.errors:
                logs.append(
                    f"[{datetime.datetime.utcnow()}] ERROR: {name} API "
                    f"Response error from {self.api_url}, {response.errors}"
                )
                self.state = ServiceConnectionState.CONNECTION_ERROR
                if self.raise_error:
                    raise ConnectionError(
                        f"[{datetime.datetime.utcnow()}] ERROR: {name} API "
                        f"Response error from {self.api_url}, "
                        f"{response.errors}"
                    )
                return False

        self.state = ServiceConnectionState.OK
        logs.append(
            f"[{datetime.datetime.utcnow()}] ServiceState = OK "
            f"for {name} {self.api_url}"
        )
        return True


class ServiceManager:
    """
    The Service Manager is a management api for a service that advertises
    the service and creates and maintains connections to other services.

    The Service Manager GraphQL API is accessible at '/service'
    """

    def __init__(
            self,
            name: str,
            schema: Any = None,
            api_version: str = None,
            connections: List[ServiceConnection] = None,
            connect_on_init: bool = True,
            connect_timeout: int = 5
    ):
        if not connections:
            connections = []

        self._connections = connections
        self.connect_on_init = connect_on_init
        self.connect_timeout = connect_timeout

        if schema is not None:
            if api_version is not None:
                raise AttributeError(
                    "api_version and schema should not both be specified. If a"
                    " service schema is provided, the api_version is taken "
                    "from that schema."
                )
            if hasattr(schema, "api_version"):
                api_version = getattr(schema, "api_version")
            else:
                raise TypeError(f"Invalid schema {schema}")

        if api_version:
            packaging_version.Version(api_version)

        self._name = name
        self._api_version = api_version
        self._started_at = datetime.datetime.now()
        self._has_checked_connections = False
        self._logs = []

        fp = os.path.dirname(
            os.path.realpath(__file__)) + '/service_manager_default.graphql'
        with open(fp, 'r') as default_query:
            default_query = default_query.read()

        self.management_http_server = GraphQLHTTPServer.from_api(
            api=GraphQLAPI(root=ServiceManager),
            serve_graphiql=True,
            allow_cors=True,
            root_value=self,
            graphiql_default_query=default_query
        )

        if self.connect_on_init:
            self.connect()

    def connect(self, timeout: int = None):
        if timeout is None:
            timeout = self.connect_timeout

        if not self._has_checked_connections and self._connections:
            self._has_checked_connections = True

            async def _check_connections(_timeout: int):
                dependencies = []
                for service in self._connections:
                    dependencies.append(
                        service.async_connect(
                            logs=self._logs,
                            timeout=_timeout
                        )
                    )
                await asyncio.gather(*dependencies)

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                loop.create_task(_check_connections(_timeout=timeout))
            else:
                asyncio.run(_check_connections(_timeout=timeout))

    def __getattr__(self, service_name):
        if self._connections:
            for service in self._connections:
                if service.name == service_name:
                    if service.state == \
                            ServiceConnectionState.CONNECTION_ERROR:
                        try:
                            loop = asyncio.get_running_loop()
                        except RuntimeError:
                            loop = None

                        if loop and loop.is_running():
                            loop.create_task(service.async_connect())
                        else:
                            asyncio.run(service.async_connect())

                    return service.remote_service_manager_api

        raise KeyError(f"Service '{service_name}' is not available.")

    def __getitem__(self, item):
        return self.__getattr__(item)

    @field
    def name(self) -> str:
        return self._name

    @field
    def api_version(self) -> str:
        return self._api_version

    @field
    def started_at(self) -> str:
        return self._started_at.strftime('%Y-%m-%d %H:%M:%S')

    @field
    def uptime(self) -> str:
        uptime = datetime.datetime.now() - self._started_at
        return str(uptime)

    @field
    def dependencies(self) -> List[ServiceConnection]:
        """
        All the Services this service is dependent on.
        :return:
        """
        return self._connections or []

    @field
    def logs(self) -> List[str]:
        return self._logs
