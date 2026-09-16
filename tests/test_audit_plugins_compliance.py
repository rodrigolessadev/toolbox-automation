"""Testes unitários para a auditoria de conformidade de plugins (5 regras e shared UI).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import audit_plugins_compliance


def setup_mock_plugin(
    root: Path,
    plugin_id: str = "plugin-teste",
    icon: str = "box",
    has_ico: bool = True,
    has_window_version: bool = True,
    has_icon_classes: bool = True,
    has_light_theme: bool = True,
    shared_ui_synced: bool = True,
    catalog_icon: Optional[str] = None,
) -> Tuple[Path, Path, Path]:
    plugins_dir = root / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    
    pdir = plugins_dir / plugin_id
    pdir.mkdir(parents=True, exist_ok=True)
    
    # 1. plugin.json
    pj = {
        "name": "Plugin Teste",
        "version": "1.0.0",
        "description": "Plugin para testes automatizados.",
        "language": "python",
        "entry": "main.py",
        "icon": icon,
        "theme_version": "material-3",
    }
    (pdir / "plugin.json").write_text(json.dumps(pj, indent=2), encoding="utf-8")
    
    # 2. catalog.json
    cat_icon = catalog_icon if catalog_icon is not None else icon
    catalog_data = {
        "plugins": [
            {
                "id": plugin_id,
                "name": "Plugin Teste",
                "version": "1.0.0",
                "icon": cat_icon,
                "theme_version": "material-3",
            }
        ]
    }
    cat_file = root / "catalog.json"
    cat_file.write_text(json.dumps(catalog_data, indent=2), encoding="utf-8")
    
    # 3. main.py
    main_code = "from shared.web_utils import create_plugin_window\n\n"
    if has_window_version:
        main_code += "window = create_plugin_window(title='Plugin Teste', entry_html='index.html', plugin_dir=PLUGIN_DIR)\n"
    else:
        main_code += "window = create_plugin_window(title='Plugin Teste', entry_html='index.html')\n"
    (pdir / "main.py").write_text(main_code, encoding="utf-8")
    
    # 4. ui/ e ui/assets/
    ui_dir = pdir / "ui"
    ui_dir.mkdir(parents=True, exist_ok=True)
    
    if has_ico:
        assets_dir = ui_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / f"{icon}.ico").write_bytes(b"\x00\x00\x01\x00\x01\x00FAKEICO")
        
    # CSS
    css_content = ":root, [data-theme=\"dark\"] { --bg: #000; }\n"
    if has_light_theme:
        css_content += "[data-theme=\"light\"] { --bg: #fff; }\n"
    if has_icon_classes:
        css_content += ".icon-sm { width: 16px; }\n.icon-md { width: 20px; }\n.btn-with-icon { gap: 8px; }\n"
        
    (ui_dir / "toolbox-theme.css").write_text(css_content, encoding="utf-8")
    (ui_dir / "icons.js").write_text("const ICONS = { box: '<svg></svg>' };", encoding="utf-8")
    
    # Shared UI
    shared_ui = plugins_dir / "shared" / "ui"
    shared_ui.mkdir(parents=True, exist_ok=True)
    
    if shared_ui_synced:
        (shared_ui / "toolbox-theme.css").write_text(css_content, encoding="utf-8")
        (shared_ui / "icons.js").write_text("const ICONS = { box: '<svg></svg>' };", encoding="utf-8")
    else:
        (shared_ui / "toolbox-theme.css").write_text("/* SHARED MESTRE DIFERENTE */", encoding="utf-8")
        (shared_ui / "icons.js").write_text("/* SHARED ICONS DIFERENTE */", encoding="utf-8")
        
    return plugins_dir, cat_file, shared_ui


def test_audit_fully_compliant_plugin(tmp_path: Path) -> None:
    """Valida um plugin que atende integralmente às 5 regras e à sincronização com shared/ui."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path)
    
    res = audit_plugins_compliance.audit_plugins(
        plugins_dir=plugins_dir,
        catalog_file=cat_file,
        shared_ui_dir=shared_ui
    )
    
    assert res["success"] is True
    assert res["total"] == 1
    assert res["passed"] == 1
    assert res["failed"] == 0
    
    plugin = res["plugins"][0]
    assert plugin["compliant"] is True
    assert plugin["rules"]["rule1_icon"]["passed"] is True
    assert plugin["rules"]["rule2_taskbar_icon"]["passed"] is True
    assert plugin["rules"]["rule3_window_version"]["passed"] is True
    assert plugin["rules"]["rule4_common_icons"]["passed"] is True
    assert plugin["rules"]["rule5_m3_dual_theme"]["passed"] is True
    assert plugin["shared_ui_sync"]["synced"] is True
    assert len(plugin["issues"]) == 0


def test_audit_detects_rule1_icon_mismatch(tmp_path: Path) -> None:
    """Valida detecção de divergência de ícone entre plugin.json e catalog.json (Regra 1)."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, icon="clock", catalog_icon="box")
    
    res = audit_plugins_compliance.audit_plugins(plugins_dir, cat_file, shared_ui)
    assert res["passed"] == 0
    plugin = res["plugins"][0]
    assert plugin["rules"]["rule1_icon"]["passed"] is False
    assert "diverge do catalog.json" in plugin["rules"]["rule1_icon"]["detail"]


def test_audit_detects_rule2_missing_taskbar_icon(tmp_path: Path) -> None:
    """Valida detecção de ausência do asset .ico na pasta ui/assets/ (Regra 2)."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, has_ico=False)
    
    res = audit_plugins_compliance.audit_plugins(plugins_dir, cat_file, shared_ui)
    assert res["passed"] == 0
    plugin = res["plugins"][0]
    assert plugin["rules"]["rule2_taskbar_icon"]["passed"] is False


def test_audit_detects_rule3_missing_window_version(tmp_path: Path) -> None:
    """Valida detecção de main.py sem vinculação de versão nem plugin_dir (Regra 3)."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, has_window_version=False)
    
    res = audit_plugins_compliance.audit_plugins(plugins_dir, cat_file, shared_ui)
    assert res["passed"] == 0
    plugin = res["plugins"][0]
    assert plugin["rules"]["rule3_window_version"]["passed"] is False


def test_audit_detects_rule4_missing_icon_classes(tmp_path: Path) -> None:
    """Valida detecção de ausência de classes utilitárias (.icon-sm) (Regra 4)."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, has_icon_classes=False)
    
    res = audit_plugins_compliance.audit_plugins(plugins_dir, cat_file, shared_ui)
    assert res["passed"] == 0
    plugin = res["plugins"][0]
    assert plugin["rules"]["rule4_common_icons"]["passed"] is False


def test_audit_detects_rule5_missing_light_theme(tmp_path: Path) -> None:
    """Valida detecção de CSS sem definição de tema claro (Regra 5)."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, has_light_theme=False)
    
    res = audit_plugins_compliance.audit_plugins(plugins_dir, cat_file, shared_ui)
    assert res["passed"] == 0
    plugin = res["plugins"][0]
    assert plugin["rules"]["rule5_m3_dual_theme"]["passed"] is False


def test_audit_detects_shared_ui_divergence(tmp_path: Path) -> None:
    """Valida detecção de desatualização de hash em relação à fonte mestre shared/ui."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, shared_ui_synced=False)
    
    res = audit_plugins_compliance.audit_plugins(plugins_dir, cat_file, shared_ui)
    plugin = res["plugins"][0]
    assert plugin["shared_ui_sync"]["synced"] is False
    assert plugin["shared_ui_sync"]["theme_synced"] is False
    assert "toolbox-theme.css desatualizado" in plugin["shared_ui_sync"]["detail"]


def test_audit_cli_json_and_strict(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Valida a execução via CLI com flags --json e --strict."""
    plugins_dir, cat_file, shared_ui = setup_mock_plugin(tmp_path, has_ico=False)
    
    # 1. Modo JSON
    code = audit_plugins_compliance.main(["--root", str(tmp_path), "--json"])
    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["success"] is True
    assert data["total"] == 1
    assert data["failed"] == 1
    
    # 2. Modo Strict com falha
    code_strict = audit_plugins_compliance.main(["--root", str(tmp_path), "--strict"])
    assert code_strict == 1
