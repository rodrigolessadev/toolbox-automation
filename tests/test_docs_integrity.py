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


def test_database_persistence_policy_exists_and_has_required_sections() -> None:
    """Valida a presença e o conteúdo da política de banco de dados SQLite Central."""
    policy = ROOT_DIR / "policies" / "database-persistence-policy.md"
    assert policy.exists(), "policies/database-persistence-policy.md deve existir"

    content = policy.read_text(encoding="utf-8")
    assert "Abordagem B" in content
    assert "com.toolbox.desktop" in content
    assert "toolbox.db" in content
    assert "shared.db_utils" in content
    assert "Namespacing de Tabelas" in content


def test_design_system_tokens_doc_exists_and_has_required_tokens() -> None:
    """Valida a existência e integridade do guia docs/design-system-tokens.md."""
    doc = ROOT_DIR / "docs" / "design-system-tokens.md"
    assert doc.exists(), "docs/design-system-tokens.md deve existir"

    content = doc.read_text(encoding="utf-8")
    assert "--bg:           #0e1014" in content or "--bg:" in content
    assert "--accent:" in content
    assert "--radius:" in content
    assert "pywebview" in content
    assert "Autossuficiência de Assets Web" in content


def test_graphify_policy_on_demand_governance() -> None:
    """Valida a inclusão da regra de atualização sob demanda no fechamento da Etapa 3."""
    policy = ROOT_DIR / "policies" / "graphify-policy.md"
    assert policy.exists(), "policies/graphify-policy.md deve existir"

    content = policy.read_text(encoding="utf-8")
    assert "Atualização Sob Demanda (Pré-Commit / Etapa 3)" in content
    assert "fechamento da implementação" in content


def test_agents_md_prompt_diet_and_token_conservation() -> None:
    """Valida se AGENTS.md mantém conformidade enxuta e referência ao docs/design-system-tokens.md."""
    agents_doc = ROOT_DIR / "AGENTS.md"
    assert agents_doc.exists(), "AGENTS.md deve existir"

    content = agents_doc.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Meta do Prompt Diet: menos de 150 linhas
    assert len(lines) < 150, f"AGENTS.md deve ter menos de 150 linhas para evitar context bloat (tem {len(lines)})"
    assert "docs/design-system-tokens.md" in content
    assert "Governança Sob Demanda do Graphify" in content
    assert "Fluxo Obrigatório de Execução" in content


