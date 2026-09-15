#!/usr/bin/env python3
"""
get_issues.py - Consulta issues abertas no GitHub para os projetos do ecossistema Toolbox.
Substitui o script legado get-issues.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

from common_utils import Colors, print_color, run_command


REPOS_MAP = {
    "toolbox": {"repo": "toolbox", "prefix": "toolbox"},
    "toolbox-plugins": {"repo": "toolbox-plugins", "prefix": "plugins"},
    "toolbox-automation": {"repo": "toolbox-automation", "prefix": "automation"},
    "toolbox-release": {"repo": "toolbox-release", "prefix": "release"},
}


def fetch_repo_issues(repo_name: str, owner: str = "rodrigolessadev") -> List[Dict[str, Any]]:
    """Consulta issues abertas no GitHub CLI para o repositório especificado."""
    full_repo = f"{owner}/{repo_name}"
    cmd = [
        "gh",
        "issue",
        "list",
        "-R",
        full_repo,
        "--state",
        "open",
        "--json",
        "number,title,labels,updatedAt,url",
        "--limit",
        "50",
    ]

    res = run_command(cmd)
    if res.returncode != 0 or not res.stdout.strip():
        return []

    try:
        data = json.loads(res.stdout)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta issues abertas no GitHub para os repositórios Toolbox.")
    parser.add_argument(
        "--project",
        choices=["all", "toolbox", "toolbox-plugins", "toolbox-automation", "toolbox-release"],
        default="all",
        help="Projeto específico ou 'all' para todos (padrão: all)",
    )
    parser.add_argument("--owner", default="rodrigolessadev", help="Proprietário dos repositórios no GitHub")
    parser.add_argument("--json", action="store_true", help="Retorna a lista completa em formato JSON")
    args = parser.parse_args()

    target_repos = (
        list(REPOS_MAP.keys()) if args.project == "all" else [args.project]
    )

    all_issues: Dict[str, List[Dict[str, Any]]] = {}

    for proj in target_repos:
        repo_info = REPOS_MAP[proj]
        issues = fetch_repo_issues(repo_info["repo"], owner=args.owner)
        all_issues[proj] = issues

    if args.json:
        print(json.dumps(all_issues, indent=2, ensure_ascii=False))
        return 0

    print_color("====================================================", Colors.CYAN)
    print_color("  Toolbox Automation - Consulta de Issues Abertas   ", Colors.CYAN)
    print_color("====================================================", Colors.CYAN)

    total_count = 0
    for proj in target_repos:
        repo_info = REPOS_MAP[proj]
        issues = all_issues.get(proj, [])
        prefix = repo_info["prefix"]
        repo_name = repo_info["repo"]

        print_color(f"\nBuscando issues abertas em {args.owner}/{repo_name}...", Colors.YELLOW)

        if not issues:
            print_color(f"Nenhuma issue aberta encontrada em {repo_name}.", Colors.GRAY)
            continue

        for item in issues:
            total_count += 1
            num = item.get("number")
            title = item.get("title")
            raw_labels = item.get("labels", [])
            labels_str = ", ".join(l.get("name", "") for l in raw_labels if isinstance(l, dict))

            print_color(f"[{prefix} #{num}] {title}", Colors.GREEN)
            if labels_str:
                print_color(f"    Labels: {labels_str}", Colors.GRAY)
            print("    Prompt rápido: ", end="")
            print_color(f"{prefix} #{num}", Colors.CYAN)

    print()
    if total_count > 0:
        print_color("Para iniciar a automação, basta copiar e enviar o 'Prompt rápido' na conversa!", Colors.MAGENTA)
    else:
        print_color("Nenhuma issue aberta encontrada nos repositórios consultados.", Colors.GRAY)

    return 0


if __name__ == "__main__":
    sys.exit(main())
