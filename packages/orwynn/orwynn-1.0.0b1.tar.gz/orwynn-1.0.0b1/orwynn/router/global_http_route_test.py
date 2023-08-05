from orwynn.apiversion import ApiVersion
from orwynn.base.module import Module
from orwynn.boot import Boot
from orwynn.http import Endpoint, HttpController


def test_default():
    """
    By default a client should use the global route.
    """
    class C(HttpController):
        ROUTE = "/message"
        ENDPOINTS = [Endpoint(method="get")]

        def get(self) -> dict:
            return {"message": "hello"}

    boot: Boot = Boot(
        root_module=Module("/user", Controllers=[C]),
        global_http_route="/donuts"
    )

    boot.app.client.get_jsonify("/user/message", 200)


def test_default_version():
    """
    By default a client should use the latest api version available.
    """
    class C(HttpController):
        ROUTE = "/message"
        ENDPOINTS = [Endpoint(method="get")]
        VERSION = 3

        def get(self) -> dict:
            return {"message": "hello"}

    boot: Boot = Boot(
        root_module=Module("/user", Controllers=[C]),
        global_http_route="/api/v{version}",
        api_version=ApiVersion(
            supported={1, 2, 3}
        )
    )

    boot.app.client.get_jsonify("/user/message", 200)


def test_not_used():
    """
    The global route can be disabled.
    """
    class C(HttpController):
        ROUTE = "/message"
        ENDPOINTS = [Endpoint(method="get")]

        def get(self) -> dict:
            return {"message": "hello"}

    boot: Boot = Boot(
        root_module=Module("/user", Controllers=[C]),
        global_http_route="/donuts"
    )

    boot.app.client.get_jsonify(
        "/donuts/user/message",
        200,
        is_global_route_used=False
    )


def test_pass_version():
    """
    A client is able to not specify global route, but pass own api version.
    """
    class C(HttpController):
        ROUTE = "/message"
        ENDPOINTS = [Endpoint(method="get")]
        VERSION = 2

        def get(self) -> dict:
            return {"message": "hello"}

    boot: Boot = Boot(
        root_module=Module("/user", Controllers=[C]),
        global_http_route="/api/v{version}",
        api_version=ApiVersion(
            supported={1, 2, 3}
        )
    )

    boot.app.client.get_jsonify(
        "/user/message",
        404,
        api_version=1
    )
    boot.app.client.get_jsonify(
        "/user/message",
        200,
        api_version=2
    )
    boot.app.client.get_jsonify(
        "/user/message",
        404,
        api_version=3
    )
