import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, registry

from gt.auth.models._auth_user_account_model import create_auth_user_account_model
from gt.auth.models._auth_user_model import create_auth_user_model
from gt.auth.models._auth_user_session_model import create_auth_user_session_model
from gt.auth.models._auth_user_tokens_model import create_auth_user_tokens_model


def _make_base():
    class Base(DeclarativeBase):
        registry = registry()

    return Base


@pytest.fixture
def models():
    """Build concrete model classes on a fresh declarative base per test."""
    base = _make_base()
    user_model = create_auth_user_model(base)
    return {
        "base": base,
        "user_model": user_model,
        "account_model": create_auth_user_account_model(base, user_model),
        "session_model": create_auth_user_session_model(base, user_model),
        "token_model": create_auth_user_tokens_model(base, user_model),
    }


@pytest.fixture
def auth():
    from gt.auth.auth import Auth

    return Auth(base=_make_base(), session_factory=async_sessionmaker[AsyncSession]())
