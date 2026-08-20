"""Quality Gate e Linter Estático de UI — Material Design 3 (M3).
Verifica:
1. Cores hardcoded (#HEX / rgb) em arquivos de estilo e componentes.
2. Contraste de cores WCAG AA (>= 4.5:1 para texto e >= 3.0:1 para componentes) em definições de tokens.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Padrão para cores hexadecimais literais
HEX_COLOR_PATTERN = re.compile(r"(?<![\w-])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGB_COLOR_PATTERN = re.compile(r"\brgba?\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+", re.IGNORECASE)

IGNORED_FILE_NAMES = {
    "tokens.json",
    "theme.css",
    "tailwind.preset.js",
    "stylelint.config.js",
    "eslint.config.js",
    "package.json",
    "package-lock.json",
    "tsconfig.json"
}

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
    "__pycache__"
}


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Converte string hex (#ffffff ou #fff) em tupla RGB (0-255)."""
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def get_relative_luminance(hex_str: str) -> float:
    """Calcula a luminância relativa sRGB conforme especificação WCAG 2.1."""
    r, g, b = [c / 255.0 for c in hex_to_rgb(hex_str)]
    
    def adjust(channel: float) -> float:
        return channel / 12.92 if channel <= 0.03928 else math.pow((channel + 0.055) / 1.055, 2.4)
        
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calcula a taxa de contraste (1:1 a 21:1) entre duas cores."""
    lum1 = get_relative_luminance(hex1)
    lum2 = get_relative_luminance(hex2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def check_tokens_contrast(tokens_data: dict) -> List[str]:
    """Valida o contraste dos pares de cores M3 em relação às diretrizes WCAG AA."""
    errors = []
    
    # Pares a serem validados (Fundo, Texto/Ícone, Contraste Mínimo)
    pairs = [
        ("primary", "onPrimary", 4.5),
        ("primaryContainer", "onPrimaryContainer", 4.5),
        ("secondary", "onSecondary", 4.5),
        ("secondaryContainer", "onSecondaryContainer", 4.5),
        ("tertiary", "onTertiary", 4.5),
        ("tertiaryContainer", "onTertiaryContainer", 4.5),
        ("error", "onError", 4.5),
        ("errorContainer", "onErrorContainer", 4.5),
        ("success", "onSuccess", 4.5),
        ("surface", "onSurface", 4.5),
        ("surfaceContainer", "onSurface", 4.5),
        ("surfaceContainerHigh", "onSurface", 4.5),
    ]
    
    for theme_mode in ["dark", "light"]:
        palette = tokens_data.get("color", {}).get(theme_mode, {})
        if not palette:
            continue
            
        for bg_key, fg_key, min_ratio in pairs:
            bg_hex = palette.get(bg_key)
            fg_hex = palette.get(fg_key)
            
            if bg_hex and fg_hex:
                ratio = calculate_contrast_ratio(bg_hex, fg_hex)
                if ratio < min_ratio:
                    errors.append(
                        f"[{theme_mode.upper()}] Contraste insuficiente entre '{bg_key}' ({bg_hex}) e '{fg_key}' ({fg_hex}): "
                        f"{ratio:.2f}:1 (Mínimo exigido: {min_ratio}:1 WCAG AA)"
                    )
                    
    return errors


def scan_file_for_hardcoded_colors(file_path: Path) -> List[str]:
    """Escaneia um arquivo de código ou estilo procurando cores literais não autorizadas."""
    if file_path.name in IGNORED_FILE_NAMES:
        return []
        
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return []
        
    violations = []
    for line_idx, line in enumerate(content.splitlines(), start=1):
        line_clean = line.strip()
        # Ignora comentários
        if line_clean.startswith("/*") or line_clean.startswith("//") or line_clean.startswith("*"):
            continue
            
        hex_matches = HEX_COLOR_PATTERN.findall(line)
        if hex_matches:
            for m in hex_matches:
                violations.append(f"Linha {line_idx}: Cor hex #{m} hardcoded encontrada. Substitua por var(--md-sys-color-*).")
                
        rgb_matches = RGB_COLOR_PATTERN.findall(line)
        if rgb_matches:
            violations.append(f"Linha {line_idx}: Função de cor direta '{rgb_matches[0]}...' encontrada.")
            
    return violations


def run_ui_linter(target_dir: Path) -> Tuple[bool, List[str]]:
    """Executa o linter de UI sobre uma pasta de projeto."""
    all_violations = []
    
    # 1. Checa tokens.json se existir
    tokens_file = target_dir / "src" / "tokens" / "tokens.json"
    if not tokens_file.exists():
        tokens_file = target_dir / "tokens.json"
        
    if tokens_file.exists():
        try:
            tokens_data = json.loads(tokens_file.read_text(encoding="utf-8"))
            contrast_errors = check_tokens_contrast(tokens_data)
            all_violations.extend(contrast_errors)
        except Exception as e:
            all_violations.append(f"Erro ao analisar {tokens_file}: {e}")
            
    # 2. Varre arquivos de estilo e código
    valid_extensions = {".css", ".scss", ".tsx", ".jsx", ".html"}
    for root, dirs, files in os.walk(target_dir):
        # Filtra pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file_name in files:
            p = Path(root) / file_name
            if p.suffix.lower() in valid_extensions:
                file_violations = scan_file_for_hardcoded_colors(p)
                for v in file_violations:
                    all_violations.append(f"{p.relative_to(target_dir)}: {v}")
                    
    passed = len(all_violations) == 0
    return passed, all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Toolbox M3 UI & Tokens Linter")
    parser.add_argument("--dir", "-d", default=".", help="Diretório a ser analisado")
    args = parser.parse_args()
    
    target = Path(args.dir).resolve()
    print(f"[UI LINTER] Analisando diretório: {target}")
    passed, violations = run_ui_linter(target)
    
    if passed:
        print("✔ [UI LINTER] Todos os arquivos estão em conformidade com o Material Design 3 e WCAG AA!")
        return 0
    else:
        print(f"✖ [UI LINTER] {len(violations)} violação(ões) encontrada(s):", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
