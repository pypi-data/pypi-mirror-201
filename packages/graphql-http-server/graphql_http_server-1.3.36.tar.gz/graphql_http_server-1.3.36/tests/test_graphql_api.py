from datetime import datetime
from typing import Optional

import pytest
from context_helper import ctx
from graphql_api import field
from requests import request, ConnectTimeout, ReadTimeout
from schemadiff.changes import CriticalityLevel
from werkzeug import Response
from werkzeug.test import Client

from graphql_http_server import GraphQLHTTPServer
from graphql_http_server.service.context import ServiceContextMiddleware
from graphql_http_server.service.manager import \
    ServiceConnection, \
    ServiceManager
from graphql_http_server.service.schema import Schema


def is_graphql_api_installed():
    try:
        import graphql_api
        assert graphql_api
    except ImportError:
        return False

    return True


def available(url, method="GET"):
    try:
        response = request(
            method,
            url,
            headers={"Accept": "text/html"},
            timeout=5,
            verify=False
        )
    except (ConnectionError, ConnectTimeout, ReadTimeout):
        return False

    if response.status_code == 400 or response.status_code == 200:
        return True

    return False


class TestGraphQLAPI:

    @pytest.mark.skipif(
        not is_graphql_api_installed(),
        reason="GraphQL-API is not installed"
    )
    def test_graphql_api(self):
        from graphql_api import GraphQLAPI

        api = GraphQLAPI()

        @api.type(root=True)
        class RootQueryType:

            @api.field
            def hello(self, name: str) -> str:
                return f"hey {name}"

        server = GraphQLHTTPServer.from_api(api=api)

        response = server.client().get('/?query={hello(name:"rob")}')

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"hey rob"}}'

    utc_time_api_url = \
        "https://europe-west2-parob-297412.cloudfunctions.net/utc_time"

    # noinspection DuplicatedCode,PyUnusedLocal
    @pytest.mark.skipif(
        not available(utc_time_api_url),
        reason=f"The UTCTime API '{utc_time_api_url}' is unavailable"
    )
    @pytest.mark.skipif(
        not is_graphql_api_installed(),
        reason="GraphQL-API is not installed"
    )
    def test_service_manager(self):
        from graphql_api import GraphQLAPI

        class UTCTimeSchema:

            @field
            def now(self) -> str:
                pass

        connections = [ServiceConnection(
            name="utc_time",
            api_url=self.utc_time_api_url,
            schema=UTCTimeSchema
        )]

        service_manager = ServiceManager(
            name="gateway",
            api_version="0.0.1",
            connections=connections
        )

        api = GraphQLAPI()

        @api.type(root=True)
        class RootQueryType:

            @api.field
            def hello(self, name: str) -> str:
                utc_time: UTCTimeSchema = ctx.services["utc_time"]

                return f"hey {name}, the time is {utc_time.now()}"

        server = GraphQLHTTPServer.from_api(api=api)

        client = Client(
            ServiceContextMiddleware(
                server.app(),
                service_manager,
                "/service"
            ),
            Response
        )

        response = client.get('/service?query={logs}')

        assert response.status_code == 200
        assert "ServiceState = OK" in response.text

        response = client.get('/?query={hello(name:"rob")}')

        assert response.status_code == 200
        assert "rob" in response.text
        assert datetime.today().strftime('%Y-%m-%d') in response.text

    @pytest.mark.skipif(
        not is_graphql_api_installed(),
        reason="GraphQL-API is not installed"
    )
    def test_schema_validation(self):
        from graphql_api import GraphQLAPI

        class UTCTime(Schema):

            @field
            def now(self) -> Optional[str]:
                raise NotImplementedError()

        class UTCTimeService(UTCTime):

            @field
            def now(self) -> Optional[str]:
                return str(datetime.now())

        server = GraphQLHTTPServer.from_api(
            api=GraphQLAPI(root=UTCTimeService)
        )

        client = Client(server.app())

        response = client.get('/?query={now}')

        assert response.status_code == 200
        assert "now" in response.text

        class InvalidUTCTimeService(UTCTime):

            @field
            def now(self) -> str:
                return str(datetime.now())

        with pytest.raises(TypeError, match="Validation Error"):
            GraphQLAPI(root=InvalidUTCTimeService).graphql_schema()

        InvalidUTCTimeService.validate_schema = False
        assert GraphQLAPI(root=InvalidUTCTimeService).graphql_schema()

        InvalidUTCTimeService.validate_schema = True
        with pytest.raises(TypeError, match="Validation Error"):
            GraphQLAPI(root=InvalidUTCTimeService).graphql_schema()

        InvalidUTCTimeService.criticality = CriticalityLevel.Breaking

        assert GraphQLAPI(root=InvalidUTCTimeService).graphql_schema()
