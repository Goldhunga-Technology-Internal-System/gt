from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gt.auth.dependencies._current_user import current_user
from gt.auth.dependencies._guards._require_access_guard import require_access
from gt.exceptions import DomainException
from gt.exceptions._base_exceptions import InvalidException, UnauthorizedException


def make_user_service(*, user_session=None, user=None):
    user_service = MagicMock()
    user_service._session_service.get_session_by = AsyncMock(return_value=user_session)
    user_service.get_user_by = AsyncMock(return_value=user)
    return user_service


class TestCurrentUser:
    async def test_returns_user_for_valid_session(self):
        user = MagicMock()
        user.is_active.return_value = True
        user_session = MagicMock()
        user_session.is_active = True
        user_service = make_user_service(user_session=user_session, user=user)

        with patch(
            "gt.auth.dependencies._current_user.get_auth_user_service",
            return_value=user_service,
        ) as get_service:
            result = await current_user(
                auth=MagicMock(), session=MagicMock(), session_uuid="valid-uuid"
            )

        assert result is user
        get_service.assert_called_once()

    async def test_raises_for_invalid_session(self):
        user_service = make_user_service(user_session=None)

        with (
            patch(
                "gt.auth.dependencies._current_user.get_auth_user_service",
                return_value=user_service,
            ),
            pytest.raises(InvalidException),
        ):
            await current_user(
                auth=MagicMock(), session=MagicMock(), session_uuid="bad-uuid"
            )

    async def test_raises_for_inactive_user(self):
        user = MagicMock()
        user.is_active.return_value = False
        user_session = MagicMock()
        user_session.is_active = True
        user_service = make_user_service(user_session=user_session, user=user)

        with (
            patch(
                "gt.auth.dependencies._current_user.get_auth_user_service",
                return_value=user_service,
            ),
            pytest.raises(InvalidException),
        ):
            await current_user(
                auth=MagicMock(), session=MagicMock(), session_uuid="valid-uuid"
            )


class TestRequireAccess:
    async def test_unauthenticated_raises(self, auth):
        dependency = require_access(auth=auth)
        request = MagicMock()
        request.cookies = {}

        with pytest.raises(UnauthorizedException):
            await dependency(request, session=MagicMock())

    async def test_returns_none_when_not_required_and_no_session(self, auth):
        dependency = require_access(auth=auth, authenticated=False)
        request = MagicMock()
        request.cookies = {}

        result = await dependency(request, session=MagicMock())

        assert result is None

    async def test_returns_user_when_authenticated(self, auth):
        user = MagicMock()
        request = MagicMock()
        request.cookies = {"session_uuid": "valid-uuid"}

        with patch(
            "gt.auth.dependencies._current_user.current_user",
            new=AsyncMock(return_value=user),
        ):
            dependency = require_access(auth=auth)
            result = await dependency(request, session=MagicMock())

        assert result is user

    async def test_email_verified_policy_is_enforced(self, auth):
        user = MagicMock()
        user.is_email_verified.return_value = False
        request = MagicMock()
        request.cookies = {"session_uuid": "valid-uuid"}

        with patch(
            "gt.auth.dependencies._current_user.current_user",
            new=AsyncMock(return_value=user),
        ):
            dependency = require_access(auth=auth, email_verified=True)
            with pytest.raises(DomainException):
                await dependency(request, session=MagicMock())
