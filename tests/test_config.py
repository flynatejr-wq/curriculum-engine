import os
import pytest
from app.config import settings

def test_settings_reads_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    from importlib import reload
    import app.config as cfg
    reload(cfg)
    assert cfg.settings.openai_api_key == "sk-test-key"

def test_settings_reads_database_url(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    from importlib import reload
    import app.config as cfg
    reload(cfg)
    assert "sqlite" in cfg.settings.database_url
