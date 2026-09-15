"""Script para sincronização de Design Tokens M3 a partir do repositório toolbox.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_AUTOMATION = Path(__file__).resolve().parent.parent
DEFAULT_TOOLBOX_TOKENS = ROOT_AUTOMATION.parent / "toolbox" / "src" / "tokens" / "tokens.json"
WEB_TEMPLATE_THEME_CSS = ROOT_AUTOMATION / "templates" / "web-react-m3" / "src" / "theme" / "theme.css"


def camel_to_kebab(s: str) -> str:
    import re
    return re.sub(r"([a-z0-9]|(?=[A-Z]))([A-Z])", r"\1-\2", s).lower()


def sync_tokens(tokens_source: Path = DEFAULT_TOOLBOX_TOKENS, target_css: Path = WEB_TEMPLATE_THEME_CSS) -> bool:
    """Lê tokens.json e atualiza theme.css no template web."""
    if not tokens_source.exists():
        print(f"✖ [SYNC] Arquivo mestre de tokens não encontrado em: {tokens_source}", file=sys.stderr)
        return False

    data = json.loads(tokens_source.read_text(encoding="utf-8"))
    
    def generate_colors(color_dict: dict) -> str:
        lines = []
        for k, v in color_dict.items():
            lines.append(f"  --md-sys-color-{camel_to_kebab(k)}: {v};")
        return "\n".join(lines)

    css = f"""/* ============================================================
   AUTO-GENERATED VIA scripts/sync_tokens.py
   Sincronizado a partir de: {tokens_source.name}
   ============================================================ */

:root, [data-theme="dark"] {{
{generate_colors(data.get("color", {}).get("dark", {}))}
}}

[data-theme="light"] {{
{generate_colors(data.get("color", {}).get("light", {}))}
}}

:root {{
"""
    for k, v in data.get("shape", {}).items():
        css += f"  --md-sys-shape-corner-{k}: {v};\n"

    for k, v in data.get("spacing", {}).items():
        css += f"  --md-sys-spacing-{k}: {v};\n"

    for k, v in data.get("elevation", {}).items():
        css += f"  --md-sys-elevation-{k}: {v};\n"

    css += "}\n"

    target_css.parent.mkdir(parents=True, exist_ok=True)
    target_css.write_text(css, encoding="utf-8")
    print(f"✔ [SYNC] Tokens M3 sincronizados com sucesso para: {target_css}")
    return True


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TOOLBOX_TOKENS
    success = sync_tokens(src)
    sys.exit(0 if success else 1)
