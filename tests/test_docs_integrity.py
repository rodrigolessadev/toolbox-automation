"""Testes de integridade da documentação oficial do Design System M3 e políticas.
"""
from __future__ import annotations

from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_design_system_md_exists_and_has_required_sections() -> None:
    """Valida a presença e o conteúdo de DESIGN-SYSTEM.md."""
    doc = ROOT_DIR / "DESIGN-SYSTEM.md"
    assert doc.exists(), "DESIGN-SYSTEM.md deve existir na raiz do repositório"

    content = doc.read_text(encoding="utf-8")
    assert "Material Design 3" in content
    assert "--md-sys-color-primary" in content
    assert "--md-sys-color-surface-container" in content
    assert "--md-sys-shape-corner" in content
    assert "WCAG AA" in content
    assert "scaffold_project.py" in content
    assert "lint_ui_tokens.py" in content


def test_ui_policy_md_exists() -> None:
    """Valida a presença da política de UI em policies/ui-design-guidelines.md."""
    policy = ROOT_DIR / "policies" / "ui-design-guidelines.md"
    assert policy.exists(), "policies/ui-design-guidelines.md deve existir"

    content = policy.read_text(encoding="utf-8")
    assert "WCAG AA" in content
    assert "Tokens Semânticos" in content
