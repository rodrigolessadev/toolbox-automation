"""
Módulo de domínio e persistência de dados do Plugin {{PLUGIN_NAME}}.
"""

from __future__ import annotations

import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def get_data_dir() -> Path:
    """Retorna o diretório base de persistência do plugin."""
    env_dir = os.environ.get("TOOLBOX_{{PLUGIN_ID_UPPER}}_DATA_DIR")
    if env_dir:
        base_dir = Path(env_dir)
    elif sys.platform == "win32" and "APPDATA" in os.environ:
        base_dir = Path(os.environ["APPDATA"]) / "com.toolbox.desktop" / "{{PLUGIN_ID}}"
    else:
        base_dir = Path.home() / ".toolbox" / "{{PLUGIN_ID}}"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_storage_file() -> Path:
    """Retorna o caminho do arquivo JSON de armazenamento de dados."""
    return get_data_dir() / "data.json"


def load_data() -> Dict[str, Any]:
    """Carrega os dados persistidos do plugin."""
    storage_file = get_storage_file()
    if not storage_file.exists():
        return {"items": []}
    try:
        content = storage_file.read_text(encoding="utf-8")
        if not content.strip():
            return {"items": []}
        return json.loads(content)
    except Exception:
        return {"items": []}


def save_data(data: Dict[str, Any]) -> bool:
    """Salva os dados do plugin no arquivo JSON de persistência."""
    try:
        storage_file = get_storage_file()
        storage_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception:
        return False


def get_items() -> List[Dict[str, Any]]:
    """Retorna a lista de itens armazenados."""
    data = load_data()
    return data.get("items", [])


def add_item(title: str, details: str = "") -> Dict[str, Any]:
    """Adiciona um novo item aos dados persistidos."""
    clean_title = (title or "").strip()
    if not clean_title:
        raise ValueError("O título não pode ser vazio.")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    import uuid
    item_id = f"item_{uuid.uuid4().hex[:8]}"

    new_item: Dict[str, Any] = {
        "id": item_id,
        "title": clean_title,
        "details": details.strip(),
        "created_at": now,
        "updated_at": now,
    }

    data = load_data()
    if "items" not in data or not isinstance(data["items"], list):
        data["items"] = []
    data["items"].insert(0, new_item)
    save_data(data)
    return new_item


def delete_item(item_id: str) -> bool:
    """Remove um item pelo seu ID."""
    data = load_data()
    items = data.get("items", [])
    initial_len = len(items)
    data["items"] = [i for i in items if i.get("id") != item_id]

    if len(data["items"]) == initial_len:
        return False

    save_data(data)
    return True
