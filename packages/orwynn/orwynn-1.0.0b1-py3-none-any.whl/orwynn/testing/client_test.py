from fastapi import Header

from orwynn._testingtools import HeadersGetHttpController
from orwynn.base.module._Module import Module
from orwynn.boot import Boot
from orwynn.http import Endpoint, HttpController
from orwynn.testing._Client import Client


class _Ctrl1(HttpController):
    ROUTE = "/"
    ENDPOINTS = [
        Endpoint(method="get")
    ]

    def get(self, x_testing: str | None = Header(default=None)) -> dict:
        return {
            "x-testing": x_testing or None
        }


class _Ctrl2(HttpController):
    ROUTE = "/"
    ENDPOINTS = [
        Endpoint(method="get")
    ]

    def get(
        self,
        x_testing: str | None = Header(default=None),
        x_tmp: str | None = Header(default=None)
    ) -> dict:
        return {
            "x-testing": x_testing or None,
            "x-tmp": x_tmp or None
        }


def test_bind_headers():
    boot: Boot = Boot(
        Module("/", Controllers=[_Ctrl1])
    )

    binded: Client = boot.app.client.bind_headers({
        "x-testing": "hello"
    })

    data: dict = binded.get_jsonify("/")
    assert data["x-testing"] == "hello"


def test_bind_headers_accumulate():
    boot: Boot = Boot(
        Module("/", Controllers=[_Ctrl2])
    )

    binded: Client = boot.app.client.bind_headers({
        "x-testing": "hello"
    }).bind_headers({
        "x-tmp": "world"
    })

    data: dict = binded.get_jsonify("/")
    assert data["x-testing"] == "hello"
    assert data["x-tmp"] == "world"

def test_multiple_bind_headers():
    """
    Shouldn't stack bind headers in the original client for subsequent
    bind_headers() calls.
    """
    boot: Boot = Boot(
        Module("/", Controllers=[HeadersGetHttpController])
    )

    binded_1: Client = boot.app.client.bind_headers({
        "x-testing": "hello"
    })

    binded_2: Client = binded_1.bind_headers({
        "x-tmp": "world"
    })

    assert binded_1.binded_headers == {"x-testing": "hello"}
    assert binded_2.binded_headers == {
        "x-testing": "hello",
        "x-tmp": "world"
    }
