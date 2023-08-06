from typing import Any, Dict, Optional

import requests
from jose import jwt

from sag_py_auth.models import AuthConfig
from sag_py_auth.token_types import JwkDict, JwksDict, TokenDict

cached_jwk: Optional[JwkDict] = None


def verify_and_decode_token(auth_config: AuthConfig, token_string: str) -> TokenDict:
    """Decode and verify the token

    Returns: The token
    """
    global cached_jwk

    if not cached_jwk:
        cached_jwk = _get_token_jwk(auth_config.issuer, token_string)

    # "decode" also verifies signature, issuer, audience, expiration and more
    token: TokenDict = jwt.decode(
        token=token_string, key=cached_jwk, audience=auth_config.audience, issuer=auth_config.issuer
    )
    return token


def _get_token_jwk(issuer: str, token_string: str) -> JwkDict:
    """Gets the key set sent from the auth provider (idp)
    that belongs to the token in the parameter. The correct
    key set is identified by key id (kid). The kid is part
    of the header information of the token.

    Returns: The key set that belongs to the token
    """

    token_header: Dict[str, Any] = jwt.get_unverified_header(token_string)
    token_key_id: str = token_header["kid"]

    auth_provider_jwks: JwksDict = _get_auth_provider_jwks(issuer)
    return auth_provider_jwks[token_key_id]


def _get_auth_provider_jwks(issuer: str) -> JwksDict:
    """Json web tokens are completely verified on the client side.
    The token is signed by the auth provider (idp) to avoid manipulation.
    To verify if the token is from the expected idp we need to request the
    public key and signing algorithm information from the idp.
    One idp can have multiple json web key sets (jwks). The key set is
    identified by the key id (kid) sent by the server.

    Returns: All key sets of the idp
    """
    jwks_request_url: str = f"{issuer}/protocol/openid-connect/certs"
    jwks_request_headers: Dict[str, str] = {"content-type": "application/json"}
    timeout_seconds = 30
    jwks_response: Dict[str, Any] = requests.get(
        jwks_request_url, headers=jwks_request_headers, timeout=timeout_seconds
    ).json()

    return {jwk["kid"]: jwk for jwk in jwks_response["keys"]}
