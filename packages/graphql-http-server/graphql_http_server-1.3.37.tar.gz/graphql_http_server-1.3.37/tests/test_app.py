import threading
import time

from urllib import request

from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from graphql_http_server import GraphQLHTTPServer


class TestApp:

    def test_dispatch(self, schema):
        server = GraphQLHTTPServer(schema=schema)

        builder = EnvironBuilder(method='GET', query_string="query={hello}")

        request = Request(builder.get_environ())
        response = server.dispatch(request=request)

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_app(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().get('/?query={hello}')

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_health_endpoint(self, schema):
        server = GraphQLHTTPServer(schema=schema, health_path="/health")
        response = server.client().get('/health')

        assert response.status_code == 200
        assert response.data == b'OK'

    def test_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().get('/', headers={"Accept": "text/html"})

        assert response.status_code == 200
        assert b'GraphiQL' in response.data

    def test_no_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema, serve_graphiql=False)
        response = server.client().get('/', headers={"Accept": "text/html"})

        assert response.status_code == 200

    def test_run_app_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema)

        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()

        time.sleep(0.5)

        req = request.Request(
            "http://localhost:5000",
            headers={"Accept": "text/html"}
        )
        response = request.urlopen(req).read()

        assert b'GraphiQL' in response
