#!/usr/bin/env python3
"""
check_projects.py - Verifica a existência e integridade dos projetos locais do ecossistema.
Substitui o script legado check-projects.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from common_utils import Colors, detect_workspace_root, print_color


PROJECTS_DEF = [
    {"name": "toolbox-automation", "required": True},
    {"name": "toolbox", "required": True},
    {"name": "toolbox-plugins", "required": True},
    {"name": "toolbox-release", "required": False},
]


def check_projects(workspace_root: Path) -> Dict[str, Any]:
    """Verifica a integridade dos repositórios dentro do workspace informado."""
    results: List[Dict[str, Any]] = []
    has_errors = False

    for item in PROJECTS_DEF:
        proj_name = item["name"]
        is_required = item["required"]
        proj_path = workspace_root / proj_name

        status: Dict[str, Any] = {
            "name": proj_name,
            "path": str(proj_path),
            "required": is_required,
            "exists": False,
            "is_git": False,
            "status": "MISSING",
        }

        if not proj_path.exists() or not proj_path.is_dir():
            if is_required:
                status["status"] = "ERROR_MISSING"
                has_errors = True
            else:
                status["status"] = "OPTIONAL_MISSING"
        else:
            status["exists"] = True
            git_dir = proj_path / ".git"
            if not git_dir.exists():
                if is_required:
                    status["status"] = "ERROR_NOT_GIT"
                    has_errors = True
                else:
                    status["status"] = "OPTIONAL_NOT_GIT"
            else:
                status["is_git"] = True
                status["status"] = "OK"

        results.append(status)

    return {
        "workspace_root": str(workspace_root),
        "success": not has_errors,
        "projects": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica os projetos locais do ecossistema Toolbox.")
    parser.add_argument("--root", type=str, default=None, help="Caminho explícito da raiz do workspace")
    parser.add_argument("--json", action="store_true", help="Retorna o resultado em formato JSON")
    args = parser.parse_args()

    workspace_root = Path(args.root).resolve() if args.root else detect_workspace_root()
    report = check_projects(workspace_root)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["success"] else 1

    print_color("====================================================", Colors.CYAN)
    print_color(f"  Toolbox Ecosystem - Verificação de Projetos Locais", Colors.CYAN)
    print_color(f"  Workspace: {workspace_root}", Colors.GRAY)
    print_color("====================================================", Colors.CYAN)

    for p in report["projects"]:
        name = p["name"]
        status = p["status"]
        print(f"Verificando projeto: {name:<22} ... ", end="")

        if status == "OK":
            print_color("[OK]", Colors.GREEN)
        elif status == "OPTIONAL_MISSING":
            print_color("[OPCIONAL - AUSENTE]", Colors.YELLOW)
        elif status == "OPTIONAL_NOT_GIT":
            print_color("[OPCIONAL - SEM GIT]", Colors.YELLOW)
        elif status == "ERROR_MISSING":
            print_color(f"[FALHA] Diretório não existe: {p['path']}", Colors.RED)
        elif status == "ERROR_NOT_GIT":
            print_color(f"[FALHA] Não é um repositório Git válido: {p['path']}", Colors.RED)

    print()
    if report["success"]:
        print_color("Todos os projetos autorizados foram verificados com sucesso.", Colors.GREEN)
        return 0
    else:
        print_color("A verificação dos projetos encontrou pendências mandatórias.", Colors.RED)
        return 1


if __name__ == "__main__":
    sys.exit(main())
