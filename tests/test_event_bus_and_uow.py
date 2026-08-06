from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from gt.auth.events._event_bus import EventBus
from gt.auth.uow._auth_uow import AuthUOW


class TestEventBus:
    async def test_register_and_publish_calls_handlers(self):
        bus = EventBus()
        received: list[str] = []

        async def handler(event):
            received.append(event)
            return event

        bus.register(str, handler)
        results = await bus.publish("hello")

        assert received == ["hello"]
        assert results == ["hello"]

    async def test_publish_with_no_handlers_returns_empty(self):
        bus = EventBus()
        assert await bus.publish("nobody-listens") == []

    async def test_before_and_after_hooks_run_in_order(self):
        bus = EventBus()
        order: list[str] = []
        bus.add_before_hook(lambda event: order.append("before"))
        bus.add_after_hook(lambda event: order.append("after"))
        bus.register(str, lambda event: order.append("handler"))

        await bus.publish("x")

        assert order == ["before", "handler", "after"]

    async def test_handler_error_is_swallowed_by_default(self):
        bus = EventBus()

        def boom(event):
            raise RuntimeError("boom")

        bus.register(str, boom)
        assert await bus.publish("x") == []

    async def test_handler_error_raises_when_requested(self):
        bus = EventBus()

        def boom(event):
            raise RuntimeError("boom")

        bus.register(str, boom)
        with pytest.raises(RuntimeError):
            await bus.publish("x", raise_on_error=True)


class TestAuthUOW:
    async def test_commits_on_success(self):
        session = SimpleNamespace(commit=AsyncMock(), rollback=AsyncMock())
        async with AuthUOW(session):
            pass
        session.commit.assert_awaited_once()
        session.rollback.assert_not_awaited()

    async def test_rolls_back_on_error(self):
        session = SimpleNamespace(commit=AsyncMock(), rollback=AsyncMock())
        with pytest.raises(ValueError):
            async with AuthUOW(session):
                raise ValueError("boom")
        session.rollback.assert_awaited_once()
        session.commit.assert_not_awaited()
