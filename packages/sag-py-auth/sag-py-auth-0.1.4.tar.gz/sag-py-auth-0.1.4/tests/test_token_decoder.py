from typing import Any, Dict

from mock import Mock
from pytest import MonkeyPatch
from requests import Response

from sag_py_auth.token_decoder import _get_token_jwk
from sag_py_auth.token_types import JwkDict


def get_mock(url: str, headers: Dict[str, str], timeout: int) -> Response:
    if (
        url == "https://authserver.com/auth/realms/projectName/protocol/openid-connect/certs"
        and headers["content-type"] == "application/json"
    ):
        return Mock(
            status_code=200,
            json=lambda: {
                "keys": [
                    {
                        "kid": "123456",
                        "kty": "RSA",
                        "alg": "RS256",
                    },
                    {
                        "kid": "654321",
                        "kty": "RSA",
                        "alg": "RS256",
                    },
                ]
            },
        )

    return Response()


def get_unverified_header_mock(token_string: str) -> Dict[str, Any]:
    return {"kid": "654321"} if token_string == "validTokenString" else {}


def test__get_token_jwk(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("sag_py_auth.token_decoder.requests.get", get_mock)
    monkeypatch.setattr("sag_py_auth.token_decoder.jwt.get_unverified_header", get_unverified_header_mock)

    # Act
    actual: JwkDict = _get_token_jwk("https://authserver.com/auth/realms/projectName", "validTokenString")

    # Assert
    assert actual == {"kid": "654321", "kty": "RSA", "alg": "RS256"}
