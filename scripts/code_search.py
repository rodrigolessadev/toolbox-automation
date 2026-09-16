#!/usr/bin/env python3
"""
code_search.py - Busca estrutural de símbolos e sintaxe no código (Python / Tree-sitter / AST).
Inspirado no ast-grep, permite localizar classes, funções e imports sem falsos positivos de regex.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from common_utils import Colors, detect_workspace_root, print_color


def search_python_ast(file_path: Path, symbol: str, sym_type: str = "all") -> List[Dict[str, Any]]:
    """Analisa a AST de um arquivo Python procurando declarações de classes, funções ou imports."""
    results: List[Dict[str, Any]] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return results

    symbol_lower = symbol.lower()

    for node in ast.walk(tree):
        # 1. Declarações de Classes
        if isinstance(node, ast.ClassDef):
            if sym_type in ("all", "class") and (symbol_lower in node.name.lower() or symbol == "*"):
                bases = []
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    elif isinstance(b, ast.Attribute):
                        bases.append(f"{getattr(b.value, 'id', '')}.{b.attr}")
                results.append({
                    "file": str(file_path),
                    "line": node.lineno,
                    "col": node.col_offset,
                    "kind": "class",
                    "name": node.name,
                    "details": f"class {node.name}({', '.join(bases)})" if bases else f"class {node.name}:",
                })

        # 2. Definições de Funções e Métodos
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if sym_type in ("all", "func") and (symbol_lower in node.name.lower() or symbol == "*"):
                args_list = [a.arg for a in node.args.args]
                is_async = isinstance(node, ast.AsyncFunctionDef)
                prefix = "async def " if is_async else "def "
                results.append({
                    "file": str(file_path),
                    "line": node.lineno,
                    "col": node.col_offset,
                    "kind": "function",
                    "name": node.name,
                    "details": f"{prefix}{node.name}({', '.join(args_list[:5])}{'...' if len(args_list) > 5 else ''})",
                })

        # 3. Imports
        elif isinstance(node, ast.ImportFrom):
            if sym_type in ("all", "import"):
                module = node.module or ""
                matched_names = [alias.name for alias in node.names if symbol_lower in alias.name.lower() or symbol_lower in module.lower()]
                if matched_names or symbol_lower in module.lower() or symbol == "*":
                    results.append({
                        "file": str(file_path),
                        "line": node.lineno,
                        "col": node.col_offset,
                        "kind": "import",
                        "name": module,
                        "details": f"from {module} import {', '.join(a.name for a in node.names)}",
                    })

    return results


def run_ast_grep_if_available(search_dir: Path, pattern: str) -> Optional[List[Dict[str, Any]]]:
    """Tenta executar ast-grep (sg) via CLI se estiver instalado no sistema."""
    sg_bin = shutil.which("sg") or shutil.which("ast-grep")
    if not sg_bin:
        return None

    cmd = [sg_bin, "run", "--pattern", pattern, "--json", str(search_dir)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            raw_data = json.loads(res.stdout)
            formatted = []
            for item in raw_data:
                formatted.append({
                    "file": item.get("file"),
                    "line": item.get("range", {}).get("start", {}).get("line", 1),
                    "col": item.get("range", {}).get("start", {}).get("column", 1),
                    "kind": "ast-grep-match",
                    "name": pattern,
                    "details": item.get("text", "").strip(),
                })
            return formatted
    except Exception:
        pass
    return None


def search_symbols(search_dir: Path, symbol: str, sym_type: str = "all", pattern: Optional[str] = None) -> List[Dict[str, Any]]:
    """Pesquisa símbolos em todos os arquivos de código suportados recursivamente."""
    if pattern:
        sg_results = run_ast_grep_if_available(search_dir, pattern)
        if sg_results is not None:
            return sg_results

    results: List[Dict[str, Any]] = []
    ignored_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", "graphify-out", ".pytest_cache"}

    for root, dirs, files in os.walk(search_dir):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for f in files:
            file_path = Path(root) / f
            if file_path.suffix == ".py":
                file_matches = search_python_ast(file_path, symbol, sym_type)
                results.extend(file_matches)

    # Ordenar por arquivo e linha
    results.sort(key=lambda x: (x["file"], x["line"]))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Busca estrutural de símbolos e sintaxe de código (AST / ast-grep).")
    parser.add_argument("--symbol", default="*", help="Nome ou fragmento do símbolo (classe, função ou import)")
    parser.add_argument("--type", choices=["all", "class", "func", "import"], default="all", help="Tipo de símbolo a buscar")
    parser.add_argument("--path", default=None, help="Diretório ou arquivo alvo para busca")
    parser.add_argument("--pattern", default=None, help="Padrão estrutural do ast-grep (ex: 'class $NAME')")
    parser.add_argument("--json", action="store_true", help="Retorna o resultado em formato JSON")
    args = parser.parse_args()

    target_dir = Path(args.path).resolve() if args.path else detect_workspace_root()
    if not target_dir.exists():
        print_color(f"[ERRO] Caminho não encontrado: {target_dir}", Colors.RED)
        return 1

    matches = search_symbols(target_dir, args.symbol, sym_type=args.type, pattern=args.pattern)

    if args.json:
        print(json.dumps(matches, indent=2, ensure_ascii=False))
        return 0

    print_color("====================================================", Colors.CYAN)
    print_color(f"  Toolbox Code Search (AST / ast-grep)               ", Colors.CYAN)
    print_color(f"  Alvo: {target_dir} | Símbolo: {args.symbol} | Tipo: {args.type}", Colors.GRAY)
    print_color("====================================================", Colors.CYAN)

    if not matches:
        print_color("Nenhum símbolo correspondente encontrado.", Colors.YELLOW)
        return 0

    workspace_root = detect_workspace_root()

    for m in matches:
        try:
            rel_file = Path(m["file"]).relative_to(workspace_root)
        except Exception:
            rel_file = Path(m["file"]).name

        kind_badge = f"[{m['kind'].upper():<8}]"
        line_info = f":{m['line']}"

        print_color(kind_badge, Colors.MAGENTA, end=" ")
        print_color(f"{rel_file}{line_info}", Colors.GREEN, end=" -> ")
        print(m["details"])

    print()
    print_color(f"Total de correspondências estruturais: {len(matches)}", Colors.CYAN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
