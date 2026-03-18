"""Тесты двусторонней синхронизации Календаря Нейропульс."""

import json
import pytest
from pathlib import Path

from src.yandex_calendar_client import (
    load_registry,
    save_registry,
    sync_neuropulse_calendar_state,
    _event_content_hash,
    _canonical_event_id,
    REGISTRY_PATH,
    PROJECT_ROOT,
)


def test_event_content_hash_deterministic():
    """Хеш содержимого события детерминирован."""
    a = {"date": "2026-04-01", "title": "X", "description": "Y", "address": ""}
    assert _event_content_hash(a) == _event_content_hash(a)
    b = {**a, "title": "Y"}
    assert _event_content_hash(a) != _event_content_hash(b)


def test_canonical_event_id_deterministic():
    """event_id для локального события детерминирован."""
    id1 = _canonical_event_id("grant", "2026-04-01", "Событие", "Описание", "grant_calendar|0")
    id2 = _canonical_event_id("grant", "2026-04-01", "Событие", "Описание", "grant_calendar|0")
    assert id1 == id2
    id3 = _canonical_event_id("grant", "2026-04-01", "Другое", "Описание", "")
    assert id1 != id3


def test_load_save_registry_roundtrip(tmp_path, monkeypatch):
    """Реестр сохраняется и загружается без потерь."""
    monkeypatch.setattr("src.yandex_calendar_client.REGISTRY_PATH", tmp_path / "registry.json")
    reg = {"last_sync": "2026-03-18T12:00:00Z", "entries": [{"event_id": "e1", "remote_uid": "u1", "status": "synced"}]}
    save_registry(reg)
    loaded = load_registry()
    assert loaded.get("last_sync") == reg["last_sync"]
    assert len(loaded.get("entries", [])) == 1
    assert loaded["entries"][0]["event_id"] == "e1"


def test_sync_returns_error_when_no_config():
    """При отсутствии calendar_url sync возвращает error в результате."""
    result = sync_neuropulse_calendar_state(calendar_url="")
    assert "error" in result
    assert result.get("created", 0) == 0
    assert result.get("updated", 0) == 0
    assert result.get("deleted", 0) == 0
    assert result.get("pulled", 0) == 0
