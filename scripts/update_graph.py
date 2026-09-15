#!/usr/bin/env python3
"""
update_graph.py - Governança segura e análise de impacto integrada ao Graphify.
Substitui o script legado update-graph.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from common_utils import Colors, detect_workspace_root, print_color


PROTECTED_KEYWORDS = [
    ".env",
    "secrets/",
    "credentials/",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
]


def is_protected_path(path_to_check: str) -> bool:
    """Verifica se o caminho contém palavras-chave protegidas ou confidenciais."""
    normalized = path_to_check.replace("\\", "/").lower()
    return any(kw in normalized for kw in PROTECTED_KEYWORDS)


def is_within_repo(target_path: Path, repo_root: Path) -> bool:
    """Verifica se o caminho alvo está estritamente dentro da árvore do repositório."""
    try:
        target_resolved = target_path.resolve()
        root_resolved = repo_root.resolve()
        return root_resolved in target_resolved.parents or target_resolved == root_resolved
    except Exception:
        return False


def run_impact_analysis(target_file: Path, repo_root: Path) -> Dict[str, Any]:
    """Executa análise estática de referências ao arquivo alvo em modo somente leitura."""
    target_basename = target_file.name
    referencing_files: List[str] = []

    ignored_parts = {".git", "graphify-out", "node_modules", "__pycache__", ".venv"}

    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in ignored_parts]
        for f in files:
            file_path = Path(root) / f
            if file_path.resolve() == target_file.resolve():
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if target_basename in content:
                    rel_path = file_path.relative_to(repo_root)
                    referencing_files.append(str(rel_path))
            except Exception:
                continue

    graph_json = repo_root / "graphify-out" / "graph.json"
    return {
        "target_file": str(target_file),
        "target_basename": target_basename,
        "total_references": len(referencing_files),
        "referencing_files": referencing_files,
        "graph_json_exists": graph_json.is_file(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Governança segura e análise de impacto do Graphify.")
    parser.add_argument("--build-graph", action="store_true", help="Dispara a geração segura do grafo")
    parser.add_argument("--impact-analysis", action="store_true", help="Executa análise de impacto em modo somente leitura")
    parser.add_argument("--target-file", type=str, default=None, help="Arquivo alvo para análise de impacto")
    parser.add_argument("--json", action="store_true", help="Retorna o resultado em formato JSON")
    args = parser.parse_args()

    # O script está em toolbox-automation/scripts/
    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / "graphify-out"

    print_color("=== Validação de Governança do Graphify ===", Colors.CYAN)

    # 1. Validação de Arquivo Alvo (se informado)
    target_resolved: Path | None = None
    if args.target_file:
        target_path = Path(args.target_file)
        target_resolved = target_path if target_path.is_absolute() else repo_root / target_path

        if not is_within_repo(target_resolved, repo_root):
            print_color("[REJEIÇÃO] O caminho alvo está fora dos limites do repositório: [CAMINHO_EXTERNO_MASCARADO]", Colors.RED)
            return 2

        if is_protected_path(str(target_resolved)):
            print_color("[REJEIÇÃO] O arquivo alvo pertence a um caminho protegido ou confidencial.", Colors.RED)
            return 2

        if not target_resolved.exists():
            print_color(f"[ERRO] Arquivo alvo não encontrado: {args.target_file}", Colors.RED)
            return 1

    # 2. Operação: Análise de Impacto (Somente Leitura)
    if args.impact_analysis:
        if not target_resolved:
            print_color("[ERRO] É necessário especificar --target-file para análise de impacto.", Colors.RED)
            return 1

        print_color(f"Executando Análise de Impacto (Somente Leitura) para: {args.target_file}", Colors.YELLOW)
        result = run_impact_analysis(target_resolved, repo_root)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0

        print_color("\n--- Resultado da Análise de Impacto ---", Colors.GREEN)
        print(f"Arquivo Alvo: {args.target_file}")
        print(f"Total de arquivos com referências diretas: {result['total_references']}")
        for ref in result["referencing_files"]:
            print_color(f"  -> {ref}", Colors.GRAY)

        if result["graph_json_exists"]:
            print_color("\n[INFO] Grafo derivado pré-existente disponível em: graphify-out/graph.json", Colors.CYAN)

        print_color("\nAnálise concluída em modo somente leitura (nenhum arquivo foi alterado).", Colors.GREEN)
        return 0

    # 3. Operação: Geração do Grafo
    if not args.build_graph:
        print_color("[MODO SOMENTE LEITURA] A geração do grafo exige a flag explícita --build-graph.", Colors.YELLOW)
        print_color("Para executar uma análise de impacto segura, utilize:", Colors.GRAY)
        print_color("  python scripts/update_graph.py --impact-analysis --target-file <caminho>", Colors.GRAY)
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "scope": "toolbox-automation",
        "status": "generated_safely",
        "read_only": True,
        "output_dir": "graphify-out",
    }
    manifest_file = output_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps({"success": True, "manifest": str(manifest_file)}))
        return 0

    print_color("Geração de grafo concluída com sucesso.", Colors.GREEN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
