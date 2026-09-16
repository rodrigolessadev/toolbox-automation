"""Testes para o motor de scaffolding e templates de projetos M3.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(SCRIPTS_DIR))

import scaffold_project
import sync_tokens


def test_scaffold_react_project(tmp_path: Path) -> None:
    """Valida a geração de um projeto React + Vite com tokens M3."""
    proj_dir = scaffold_project.scaffold_project("react-m3", "test-plugin-app", tmp_path)
    assert proj_dir.exists()

    pkg_json = proj_dir / "package.json"
    assert pkg_json.exists()
    assert '"name": "test-plugin-app"' in pkg_json.read_text(encoding="utf-8")

    theme_css = proj_dir / "src" / "theme" / "theme.css"
    assert theme_css.exists()
    assert "--md-sys-color-primary" in theme_css.read_text(encoding="utf-8")

    theme_prov = proj_dir / "src" / "theme" / "ThemeProvider.tsx"
    assert theme_prov.exists()
    assert "useTheme" in theme_prov.read_text(encoding="utf-8")


def test_scaffold_streamlit_project(tmp_path: Path) -> None:
    """Valida a geração de um Data App Streamlit com tema M3."""
    proj_dir = scaffold_project.scaffold_project("streamlit-m3", "test-data-app", tmp_path)
    assert proj_dir.exists()

    config_toml = proj_dir / ".streamlit" / "config.toml"
    assert config_toml.exists()
    content = config_toml.read_text(encoding="utf-8")
    assert 'primaryColor = "#a8c7fa"' in content
    assert 'backgroundColor = "#111318"' in content

    app_py = proj_dir / "app.py"
    assert app_py.exists()
    assert "Material Design 3" in app_py.read_text(encoding="utf-8")


def test_scaffold_plugin_pywebview(tmp_path: Path) -> None:
    """Valida a geração de um novo plugin pywebview autossuficiente para o ecossistema Toolbox."""
    test_dir = tmp_path / "tests"
    plugin_dir = scaffold_project.scaffold_project(
        template_type="plugin-pywebview",
        project_name="Calculadora de Horas",
        output_dir=tmp_path,
        plugin_id="calc-horas",
        plugin_icon="clock",
        plugin_description="Cálculo de horas trabalhadas e jornadas.",
        test_output_dir=test_dir,
    )

    assert plugin_dir.exists()
    assert plugin_dir.name == "calc-horas"

    # 1. Valida manifesto plugin.json
    pj = plugin_dir / "plugin.json"
    assert pj.exists()
    pj_data = json.loads(pj.read_text(encoding="utf-8"))
    assert pj_data["name"] == "Calculadora de Horas"
    assert pj_data["icon"] == "clock"
    assert pj_data["entry"] == "main.py"
    assert pj_data["version"] == "1.0.0"
    assert pj_data["theme_version"] == "material-3"
    assert pj_data["description"] == "Cálculo de horas trabalhadas e jornadas."

    # 2. Valida package.json
    pkg = plugin_dir / "package.json"
    assert pkg.exists()
    pkg_data = json.loads(pkg.read_text(encoding="utf-8"))
    assert pkg_data["name"] == "@toolbox-plugins/calc-horas"
    assert "@toolbox-plugins/shared-markdown" in pkg_data["dependencies"]

    # 3. Valida domain.py e sintaxe Python
    domain_file = plugin_dir / "domain.py"
    assert domain_file.exists()
    domain_content = domain_file.read_text(encoding="utf-8")
    assert "TOOLBOX_CALC_HORAS_DATA_DIR" in domain_content
    assert "calc-horas" in domain_content
    # Valida sintaxe sem erros
    ast.parse(domain_content)

    # 4. Valida main.py e classe PascalCase
    main_file = plugin_dir / "main.py"
    assert main_file.exists()
    main_content = main_file.read_text(encoding="utf-8")
    assert "class CalcHorasApi(BasePluginApi):" in main_content
    assert "calc-horas_domain" in main_content
    assert "plugin_dir=PLUGIN_DIR" in main_content
    ast.parse(main_content)

    # 5. Valida autossuficiência de assets web e ícone de taskbar
    ui_dir = plugin_dir / "ui"
    assert ui_dir.exists()
    assert (ui_dir / "index.html").exists()
    assert (ui_dir / "style.css").exists()
    assert (ui_dir / "icons.js").exists()
    assert (ui_dir / "toolbox-theme.css").exists()
    assert (ui_dir / "app.js").exists()

    # Valida asset .ico gerado na pasta ui/assets/
    assets_dir = ui_dir / "assets"
    assert assets_dir.exists()
    ico_file = assets_dir / "clock.ico"
    assert ico_file.exists()
    assert ico_file.stat().st_size > 0

    # Valida classes utilitárias de ícones M3 no CSS
    theme_css = (ui_dir / "toolbox-theme.css").read_text(encoding="utf-8")
    assert ".icon-sm" in theme_css
    assert ".icon-md" in theme_css
    assert ".icon-lg" in theme_css
    assert ".btn-with-icon" in theme_css

    # Valida catálogo expandido de ícones
    icons_js = (ui_dir / "icons.js").read_text(encoding="utf-8")
    assert "'sun':" in icons_js
    assert "'moon':" in icons_js
    assert "'settings':" in icons_js

    html_content = (ui_dir / "index.html").read_text(encoding="utf-8")
    assert "Calculadora de Horas" in html_content
    assert 'data-icon="clock"' in html_content

    # 6. Valida arquivo de testes gerado no diretório alvo
    test_file = test_dir / "test_plugin_calc_horas.py"
    assert test_file.exists()
    test_content = test_file.read_text(encoding="utf-8")
    assert "calc-horas" in test_content
    assert "CalcHorasApi" in test_content
    ast.parse(test_content)


def test_scaffold_plugin_pywebview_auto_id(tmp_path: Path) -> None:
    """Valida a derivação automática de plugin_id e nomes a partir do project_name."""
    plugin_dir = scaffold_project.scaffold_project(
        template_type="pywebview-m3",
        project_name="Monitor de Rede",
        output_dir=tmp_path,
    )
    assert plugin_dir.exists()
    assert plugin_dir.name == "monitor-de-rede"

    pj_data = json.loads((plugin_dir / "plugin.json").read_text(encoding="utf-8"))
    assert pj_data["name"] == "Monitor de Rede"
    assert pj_data["icon"] == "box"

    main_content = (plugin_dir / "main.py").read_text(encoding="utf-8")
    assert "class MonitorDeRedeApi(BasePluginApi):" in main_content
    assert "plugin_dir=PLUGIN_DIR" in main_content

    # Valida .ico padrão gerado
    assert (plugin_dir / "ui" / "assets" / "box.ico").exists()


def test_scaffold_plugin_copies_shared_ui_when_in_plugins_repo(tmp_path: Path) -> None:
    """Valida que novos plugins scaffolded dentro de repositório de plugins herdam a fonte mestre de UI."""
    plugins_root = tmp_path / "plugins"
    shared_ui = plugins_root / "shared" / "ui"
    shared_ui.mkdir(parents=True, exist_ok=True)

    master_css = "/* MESTRE SHARED TEST CSS */\n:root { --master-token: #123456; }"
    master_icons = "/* MESTRE ICONS TEST JS */\nconst ICONS = { master: '<svg></svg>' };"
    (shared_ui / "toolbox-theme.css").write_text(master_css, encoding="utf-8")
    (shared_ui / "icons.js").write_text(master_icons, encoding="utf-8")

    plugin_dir = scaffold_project.scaffold_project(
        template_type="plugin-pywebview",
        project_name="Plugin Sincronizado",
        output_dir=plugins_root,
        plugin_id="plugin-sincronizado",
        plugin_icon="box",
    )

    assert plugin_dir.exists()
    ui_dir = plugin_dir / "ui"

    # Deve ter copiado diretamente da fonte mestre
    assert (ui_dir / "toolbox-theme.css").read_text(encoding="utf-8") == master_css
    assert (ui_dir / "icons.js").read_text(encoding="utf-8") == master_icons
    assert (ui_dir / "assets" / "box.ico").exists()



def test_sync_tokens_from_file(tmp_path: Path) -> None:
    """Valida a sincronização de tokens a partir de um arquivo JSON."""
    fake_tokens = tmp_path / "tokens.json"
    fake_tokens.write_text("""{
      "color": {
        "dark": { "primary": "#123456" },
        "light": { "primary": "#654321" }
      },
      "shape": { "xs": "4px" },
      "elevation": { "level1": "none" }
    }""", encoding="utf-8")

    target_css = tmp_path / "theme.css"
    success = sync_tokens.sync_tokens(fake_tokens, target_css)
    assert success is True
    assert target_css.exists()

    css_text = target_css.read_text(encoding="utf-8")
    assert "--md-sys-color-primary: #123456;" in css_text
    assert "--md-sys-shape-corner-xs: 4px;" in css_text
