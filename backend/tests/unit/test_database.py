import pytest
from importlib import reload


# ---------------------------
# Test Environment Variable Loading and Session Creation
# ---------------------------


def test_env_loading(monkeypatch):
    """Test that DATABASE_URL is loaded correctly when set."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    import api.database as db

    reload(db)

    assert db.DATABASE_URL == "sqlite:///:memory:"
    assert db.engine is not None
    assert db.SessionLocal is not None


def test_missing_database_url(monkeypatch):
    """Test that ValueError is raised if DATABASE_URL is not set."""
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(
        ValueError, match="DATABASE_URL environment variable is not set."
    ):
        import api.database as db

        reload(db)


def test_session_lifecycle(monkeypatch):
    """Test session can be created and closed successfully."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    import api.database as db

    reload(db)

    session = db.SessionLocal()
    assert session is not None
    session.close()


def test_env_warning_on_missing_dotenv(monkeypatch):
    """Test warning print when dotenv is missing (simulate ImportError)."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    import builtins

    original_import = builtins.__import__

    def mocked_import(name, *args, **kwargs):
        if name == "dotenv":
            raise ImportError("dotenv not found")
        return original_import(name, *args, **kwargs)

    builtins.__import__ = mocked_import

    try:
        import api.database as db

        reload(db)
        assert db.DATABASE_URL == "sqlite:///:memory:"
    finally:
        builtins.__import__ = original_import
