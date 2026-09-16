import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PLUGIN_DIR = Path(__file__).resolve().parent
if str(PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_DIR))
PLUGINS_ROOT = PLUGIN_DIR.parent
if str(PLUGINS_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGINS_ROOT))

import importlib.util
from shared.web_utils import BasePluginApi, create_plugin_window

try:
    import webview
except ImportError:
    webview = None

domain_path = PLUGIN_DIR / "domain.py"
spec = importlib.util.spec_from_file_location("{{PLUGIN_ID}}_domain", domain_path)
domain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(domain)


class {{PLUGIN_NAME_PASCAL}}Api(BasePluginApi):
    """API exposta para a interface WebView do plugin {{PLUGIN_NAME}}."""

    def get_items(self) -> Dict[str, Any]:
        """Retorna todos os itens persistidos."""
        try:
            return {"success": True, "items": domain.get_items()}
        except Exception as exc:
            return {"success": False, "error": str(exc), "items": []}

    def add_item(self, title: str, details: str = "") -> Dict[str, Any]:
        """Adiciona um novo item."""
        try:
            item = domain.add_item(title=title, details=details)
            return {"success": True, "item": item, "items": domain.get_items()}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def delete_item(self, item_id: str) -> Dict[str, Any]:
        """Exclui um item."""
        try:
            success = domain.delete_item(item_id=item_id)
            return {"success": success, "items": domain.get_items()}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def get_plugin_version(self) -> Dict[str, Any]:
        """Retorna a versão do plugin declarada no plugin.json."""
        try:
            pj = PLUGIN_DIR / "plugin.json"
            if pj.exists():
                data = json.loads(pj.read_text(encoding="utf-8"))
                return {"success": True, "version": data.get("version", "1.0.0")}
        except Exception:
            pass
        return {"success": True, "version": "1.0.0"}


def main():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("toolbox.plugin.{{PLUGIN_ID}}")
        except Exception:
            pass

    api = {{PLUGIN_NAME_PASCAL}}Api()
    ui_index = Path(__file__).parent / "ui" / "index.html"
    window = create_plugin_window(
        title="{{PLUGIN_NAME}}",
        entry_html=ui_index,
        js_api=api,
        plugin_dir=PLUGIN_DIR,
        width=960,
        height=700,
        min_size=(680, 520),
    )

    if webview:
        webview.start(debug=False)


if __name__ == "__main__":
    main()
