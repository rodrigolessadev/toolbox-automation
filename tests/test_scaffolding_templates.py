"""Testes para o motor de scaffolding e templates de projetos M3.
"""
from __future__ import annotations

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
