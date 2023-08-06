from contextvars import ContextVar
from typing import Optional

from sag_py_auth.models import Token

token: ContextVar[Optional[Token]] = ContextVar("token", default=None)


def get_token() -> Optional[Token]:
    """Gets the context local token. See library contextvars for details.

    Returns: The token
    """
    return token.get(None)


def set_token(token_to_set: Token) -> None:
    """Sets the context local token. See library contextvars for details."""
    token.set(token_to_set)
