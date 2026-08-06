import pytest

from gt.auth.services.hash._hash_service import HasherService


@pytest.fixture(scope="class")
def hasher() -> HasherService:
    return HasherService()


class TestHasherService:
    def test_hash_and_verify(self, hasher: HasherService):
        hashed = hasher.hash("secret-password")
        assert hashed != "secret-password"
        assert hasher.verify(hashed, "secret-password") is True

    def test_verify_wrong_password(self, hasher: HasherService):
        hashed = hasher.hash("secret-password")
        assert hasher.verify(hashed, "wrong-password") is False

    def test_verify_invalid_hash_returns_false(self, hasher: HasherService):
        assert hasher.verify("not-a-valid-hash", "secret-password") is False

    def test_deterministic_hash_is_stable(self, hasher: HasherService):
        hashed = hasher.deterministic_hash("abc")
        assert hashed == hasher.deterministic_hash("abc")
        assert hasher.verify_deterministic_hash("abc", hashed) is True

    def test_deterministic_hash_changes_with_input(self, hasher: HasherService):
        assert hasher.deterministic_hash("abc") != hasher.deterministic_hash("abd")

    def test_verify_deterministic_hash_rejects_wrong_value(self, hasher: HasherService):
        other = hasher.deterministic_hash("abd")
        assert hasher.verify_deterministic_hash("abc", other) is False
