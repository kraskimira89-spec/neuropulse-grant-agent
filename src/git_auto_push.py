"""
Автоотправка в Git после значительных изменений и при завершении процесса.
Добавляются только безопасные пути (без секретов).
"""

from __future__ import annotations

import atexit
import logging
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)

# Пути, которые считаем «значительными» (только они участвуют в автокоммите)
SIGNIFICANT_PREFIXES = (
    "src/",
    "docs/",
    "scripts/",
    "Паспорт/",
    "config/config.json",
    ".env.example",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    ".gitignore",
)


def _run(cmd: list[str], timeout_sec: int = 30) -> tuple[bool, str]:
    """Запускает команду в корне проекта. Возвращает (успех, вывод)."""
    try:
        r = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_sec,
        )
        out = (r.stdout or "").strip() + "\n" + (r.stderr or "").strip()
        return r.returncode == 0, out
    except subprocess.TimeoutExpired:
        logger.warning("Git: таймаут команды %s", cmd)
        return False, "timeout"
    except Exception as e:
        logger.warning("Git: ошибка запуска %s: %s", cmd, e)
        return False, str(e)


def _has_significant_changes() -> bool:
    """Проверяет, есть ли изменения в значимых путях (по git status)."""
    ok, out = _run(["git", "status", "--short"])
    if not ok:
        return False
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        # " M src/..." или "?? Паспорт/..."
        path = line.split(maxsplit=1)[-1] if len(line.split()) >= 2 else line
        path = path.strip('"').replace("\\", "/")
        if any(path == p or path.startswith(p.rstrip("/") + "/") for p in SIGNIFICANT_PREFIXES):
            return True
    return False


def git_push_if_changes(commit_message: str | None = None) -> bool:
    """
    Если есть значимые изменения: git add, commit, push.
    Возвращает True, если коммит и push выполнены, иначе False.
    """
    if not _has_significant_changes():
        return False
    add_cmd = ["git", "add"] + list(SIGNIFICANT_PREFIXES)
    ok, _ = _run(add_cmd)
    if not ok:
        return False
    # Проверяем, что после add что-то в индексе
    ok, out = _run(["git", "diff", "--cached", "--quiet"])
    if ok:
        return False
    msg = commit_message or "Автосохранение: изменения проекта"
    ok, out = _run(["git", "commit", "-m", msg])
    if not ok:
        logger.warning("Git commit не удался: %s", out)
        return False
    ok, out = _run(["git", "push"])
    if not ok:
        logger.warning("Git push не удался: %s", out)
        return False
    logger.info("Git: автоотправка выполнена")
    return True


def _register_atexit() -> None:
    """Один раз регистрирует при выходе процесса попытку отправить изменения в Git."""
    def _on_exit() -> None:
        git_push_if_changes(commit_message="Автосохранение перед завершением")

    atexit.register(_on_exit)
