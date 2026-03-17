"""
Заполняет data/grant_contacts.json контактами из заявки на грант (.docx).
Ищет в документе таблицу с командой (столбцы: ФИО/Имя, Должность/Роль, Email).

Использование:
  python scripts/fill_contacts_from_application.py путь/к/заявка.docx
  python scripts/fill_contacts_from_application.py   # ищет data/заявка.docx или Паспорт/заявка.docx
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Корень проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CONTACTS_PATH = PROJECT_ROOT / "data" / "grant_contacts.json"


def extract_contacts_from_docx(docx_path: Path) -> list[dict]:
    """Извлекает контакты из таблиц в .docx (команда/специалисты)."""
    from docx import Document

    doc = Document(str(docx_path))
    NAME_KEYS = ("фио", "ф.и.о", "имя", "фам")
    ROLE_KEYS = ("должность", "роль", "позиция", "функция", "обязанност")
    EMAIL_KEYS = ("email", "e-mail", "почта", "эл. почта", "электронная почта")

    def col_index(row_cells, keys_tuple) -> int | None:
        for i, cell in enumerate(row_cells):
            t = (cell.text or "").strip().lower()
            for k in keys_tuple:
                if k in t:
                    return i
        return None

    for table in doc.tables:
        if not table.rows:
            continue
        header = table.rows[0].cells
        i_name = col_index(header, NAME_KEYS)
        i_role = col_index(header, ROLE_KEYS)
        i_email = col_index(header, EMAIL_KEYS)
        if i_name is None and i_role is None:
            continue
        if i_name is None:
            i_name = 0
        if i_role is None:
            i_role = i_name + 1 if len(header) > i_name + 1 else i_name
        if i_email is None:
            i_email = max(i_name, i_role) + 1 if len(header) > max(i_name, i_role) + 1 else i_role

        out = []
        for row in table.rows[1:]:
            cells = row.cells
            n = len(cells)
            name = (cells[i_name].text or "").strip() if n > i_name else ""
            role = (cells[i_role].text or "").strip() if n > i_role else ""
            email = (cells[i_email].text or "").strip() if n > i_email else ""
            if name or role or email:
                out.append({"name": name or "—", "role": role or "—", "email": email or "—"})
        if out:
            return out
    return []


def main() -> None:
    if len(sys.argv) >= 2:
        path = Path(sys.argv[1])
    else:
        for candidate in [PROJECT_ROOT / "data" / "заявка.docx", PROJECT_ROOT / "Паспорт" / "заявка.docx"]:
            if candidate.exists():
                path = candidate
                break
        else:
            print("Укажите путь к .docx заявки или положите файл data/заявка.docx", file=sys.stderr)
            sys.exit(1)

    if not path.exists():
        print(f"Файл не найден: {path}", file=sys.stderr)
        sys.exit(1)

    contacts = extract_contacts_from_docx(path)
    if not contacts:
        print("В документе не найдена таблица с командой (ФИО, Должность, Email).", file=sys.stderr)
        sys.exit(1)

    CONTACTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTACTS_PATH, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print(f"Сохранено контактов: {len(contacts)} в {CONTACTS_PATH}")


if __name__ == "__main__":
    main()
