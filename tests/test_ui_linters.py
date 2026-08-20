"""Testes para validação de regras de linter de UI, detecção de cores hardcoded e contraste WCAG AA.
"""
from __future__ import annotations

import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(SCRIPTS_DIR))

import lint_ui_tokens


def test_contrast_ratio_calculation() -> None:
    """Valida o cálculo da taxa de contraste entre cores conhecidas."""
    # Branco (#ffffff) vs Preto (#000000) = 21:1
    ratio = lint_ui_tokens.calculate_contrast_ratio("#ffffff", "#000000")
    assert round(ratio, 1) == 21.0

    # Mesma cor = 1:1
    ratio_same = lint_ui_tokens.calculate_contrast_ratio("#123456", "#123456")
    assert round(ratio_same, 1) == 1.0


def test_tokens_contrast_validation() -> None:
    """Valida a detecção de contraste insuficiente em tokens."""
    bad_tokens = {
        "color": {
            "dark": {
                "primary": "#121212",      # Fundo escuro
                "onPrimary": "#1a1a1a"     # Texto quase da mesma cor (contraste ~1.1:1)
            }
        }
    }
    errors = lint_ui_tokens.check_tokens_contrast(bad_tokens)
    assert len(errors) > 0
    assert "Contraste insuficiente" in errors[0]

    good_tokens = {
        "color": {
            "dark": {
                "primary": "#a8c7fa",      # Fundo azul claro
                "onPrimary": "#062e6f"     # Texto azul muito escuro (contraste > 8:1)
            }
        }
    }
    no_errors = lint_ui_tokens.check_tokens_contrast(good_tokens)
    assert len(no_errors) == 0


def test_scan_file_detects_hardcoded_hex(tmp_path: Path) -> None:
    """Valida que o linter flagra cores hexadecimais em arquivos regulares."""
    bad_css = tmp_path / "custom.css"
    bad_css.write_text("""
    .my-button {
      background-color: #3a7bff;
      color: #ffffff;
    }
    """, encoding="utf-8")

    violations = lint_ui_tokens.scan_file_for_hardcoded_colors(bad_css)
    assert len(violations) >= 2
    assert any("#3a7bff" in v for v in violations)


def test_scan_file_passes_clean_tokenized_css(tmp_path: Path) -> None:
    """Valida que arquivos usando variáveis CSS semânticas são aprovados com louvor."""
    good_css = tmp_path / "clean.css"
    good_css.write_text("""
    .my-button {
      background-color: var(--md-sys-color-primary);
      color: var(--md-sys-color-on-primary);
    }
    """, encoding="utf-8")

    violations = lint_ui_tokens.scan_file_for_hardcoded_colors(good_css)
    assert len(violations) == 0
