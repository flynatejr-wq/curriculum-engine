import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None)
    database_url: str
    openai_api_key: str


def test_settings_reads_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    s = Settings()
    assert s.openai_api_key == "sk-test-key"


def test_settings_reads_database_url(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    s = Settings()
    assert s.database_url == "sqlite+aiosqlite:///./test.db"


def test_settings_raises_on_missing_vars(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    # Ensure .env is not loaded during this test
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        Settings()
