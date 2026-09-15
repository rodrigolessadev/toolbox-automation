#!/usr/bin/env python3
"""
load_context.py - Carrega e valida o contexto persistente da automação.
Substitui o script legado load-context.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from common_utils import Colors, print_color


REQUIRED_CONTEXT_FILES = [
    "project-context.md",
    "architecture-overview.md",
    "decisions.md",
    "handoff.md",
    "work-log.md",
]


def validate_context(agent_dir: Path, with_graph: bool = False) -> Dict[str, Any]:
    """Verifica a presença dos arquivos mandatórios de contexto persistente."""
    if not agent_dir.exists() or not agent_dir.is_dir():
        return {
            "success": False,
            "error": f"Diretório de contexto {agent_dir} não encontrado.",
            "files": [],
        }

    files_status: List[Dict[str, Any]] = []
    missing_count = 0

    for fname in REQUIRED_CONTEXT_FILES:
        target = agent_dir / fname
        exists = target.is_file()
        if not exists:
            missing_count += 1
        files_status.append({
            "name": fname,
            "path": str(target),
            "exists": exists,
        })

    graph_status = None
    if with_graph:
        graph_file = Path("graphify-out/graph.json")
        graph_status = {
            "path": str(graph_file),
            "exists": graph_file.is_file(),
        }

    return {
        "success": missing_count == 0,
        "agent_dir": str(agent_dir),
        "missing_count": missing_count,
        "files": files_status,
        "graph": graph_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Carrega e valida os arquivos de contexto persistente do agente.")
    parser.add_argument("--dir", default=".agent", help="Diretório de contexto do agente (padrão: .agent)")
    parser.add_argument("--with-graph", action="store_true", help="Verifica também o grafo gerado pelo Graphify")
    parser.add_argument("--json", action="store_true", help="Retorna o relatório em formato JSON")
    args = parser.parse_args()

    agent_dir = Path(args.dir)
    report = validate_context(agent_dir, with_graph=args.with_graph)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["success"] else 1

    print_color("Carregando contexto persistente da automação...", Colors.CYAN)

    if "error" in report:
        print_color(f"[ERRO] {report['error']}", Colors.RED)
        return 1

    for f in report["files"]:
        if f["exists"]:
            print_color(f"[OK] Contexto carregado: {f['name']}", Colors.GREEN)
        else:
            print_color(f"[FALHA] Arquivo de contexto ausente: {f['name']}", Colors.RED)

    if args.with_graph and report.get("graph"):
        if report["graph"]["exists"]:
            print_color("[GRAPHIFY] Grafo estrutural detectado e carregado em modo somente leitura.", Colors.CYAN)
        else:
            print_color("[GRAPHIFY] Grafo derivado não encontrado (operação continua normalmente).", Colors.YELLOW)

    if not report["success"]:
        print_color("Contexto persistente incompleto.", Colors.RED)
        return 1

    print_color("Contexto carregado com sucesso.", Colors.GREEN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
