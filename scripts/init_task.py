#!/usr/bin/env python3
"""
init_task.py - Inicializa o ciclo de vida de uma tarefa a partir de uma issue do GitHub.
Substitui o script legado init-task-from-issue.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from common_utils import (
    Colors,
    detect_workspace_root,
    get_project_path,
    print_color,
    run_command,
)
from start_task import create_task_checkpoint


def fetch_issue_data(repo: str, issue_number: int, owner: str = "rodrigolessadev") -> Dict[str, Any]:
    """Consulta os dados estruturados de uma issue via GitHub CLI."""
    full_repo = f"{owner}/{repo}"
    cmd = [
        "gh",
        "issue",
        "view",
        str(issue_number),
        "--repo",
        full_repo,
        "--json",
        "number,title,body,labels",
    ]
    res = run_command(cmd)
    if res.returncode != 0 or not res.stdout.strip():
        raise RuntimeError(f"Não foi possível consultar a issue #{issue_number} via GitHub CLI: {res.stderr.strip()}")

    return json.loads(res.stdout)


def slugify(text: str, max_len: int = 40) -> str:
    """Gera um slug curto e semântico para nomes de branch."""
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    if len(clean) > max_len:
        clean = clean[:max_len].rstrip("-")
    return clean or "task"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inicializa uma tarefa de automação a partir de issue do GitHub.")
    parser.add_argument("--repo", required=True, choices=["toolbox", "toolbox-plugins", "toolbox-automation", "toolbox-release"], help="Repositório alvo")
    parser.add_argument("--issue", type=int, required=True, help="Número da issue")
    parser.add_argument("--owner", default="rodrigolessadev", help="Proprietário no GitHub")
    parser.add_argument("--no-branch", action="store_true", help="Não cria a branch no repositório local")
    parser.add_argument("--json", action="store_true", help="Retorna os dados da tarefa em formato JSON")
    args = parser.parse_args()

    print_color(f"Buscando informações da issue #{args.issue} no repositório {args.owner}/{args.repo}...", Colors.CYAN)

    try:
        issue_data = fetch_issue_data(args.repo, args.issue, owner=args.owner)
    except Exception as e:
        print_color(f"[ERRO] {e}", Colors.RED)
        return 1

    title = issue_data.get("title", "")
    body = issue_data.get("body", "")
    labels = [l.get("name", "") if isinstance(l, dict) else str(l) for l in issue_data.get("labels", [])]

    print_color(f"Issue encontrada: #{args.issue} - {title}", Colors.GREEN)

    # Classificação do tipo de tarefa
    task_type = "feature"
    workflow = "new-feature"
    branch_prefix = "feat"

    is_bug = any("bug" in l.lower() or "fix" in l.lower() for l in labels) or bool(
        re.search(r"\b(bug|fix|correção|erro)\b", title, re.IGNORECASE)
    )

    if is_bug:
        task_type = "bug_fix"
        workflow = "bug-fix"
        branch_prefix = "fix"
    elif args.repo == "toolbox-plugins":
        task_type = "plugin"
        workflow = "plugin-lifecycle"
        branch_prefix = "feat"

    task_id = f"TASK-{args.repo}-{args.issue}"
    slug = slugify(title)
    branch_name = f"{branch_prefix}/issue-{args.issue}-{slug}"

    # 1. Salvar Request estruturado em .agent/requests/
    requests_dir = Path(".agent/requests")
    requests_dir.mkdir(parents=True, exist_ok=True)
    request_file = requests_dir / f"{task_id}.json"

    task_request: Dict[str, Any] = {
        "task_id": task_id,
        "issue_number": args.issue,
        "repository": args.repo,
        "title": title,
        "description": body,
        "task_type": task_type,
        "workflow": workflow,
        "labels": labels,
        "branch": branch_name,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    request_file.write_text(json.dumps(task_request, indent=2, ensure_ascii=False), encoding="utf-8")
    print_color(f"Requisição estruturada salva em: {request_file}", Colors.GREEN)

    # 2. Iniciar checkpoint
    checkpoints_dir = Path(".agent/checkpoints")
    create_task_checkpoint(
        task_id=task_id,
        description=f"Issue #{args.issue} - {title}",
        checkpoints_dir=checkpoints_dir,
        metadata={"branch": branch_name, "workflow": workflow},
    )

    # 3. Configurar branch no repositório de destino
    target_repo_path = get_project_path(args.repo)
    if not args.no_branch and target_repo_path.exists() and (target_repo_path / ".git").exists():
        print_color(f"Configurando branch {branch_name} em {target_repo_path}...", Colors.CYAN)
        res_branch = run_command(["git", "checkout", "-B", branch_name], cwd=target_repo_path)
        if res_branch.returncode == 0:
            print_color(f"Branch configurada com sucesso: {branch_name}", Colors.GREEN)
        else:
            print_color(f"[AVISO] Falha ao alternar branch git: {res_branch.stderr.strip()}", Colors.YELLOW)

    # 4. Atualizar estado local do Kanban (se existir)
    workspace_root = detect_workspace_root()
    state_file = workspace_root / "toolbox" / ".release_plugin_state" / "state.json"
    if state_file.exists():
        try:
            state_data = json.loads(state_file.read_text(encoding="utf-8"))
            if "issues" not in state_data or not isinstance(state_data["issues"], dict):
                state_data["issues"] = {}

            issue_key = f"{args.repo}#{args.issue}"
            state_data["issues"][issue_key] = {
                "repo": args.repo,
                "issue_number": args.issue,
                "branch": branch_name,
                "last_status": "🛠 Em andamento",
                "updated_at": datetime.datetime.now().isoformat(),
            }
            state_file.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print_color(f"Kanban local atualizado: {issue_key} -> 🛠 Em andamento", Colors.GREEN)
        except Exception as ex:
            print_color(f"[AVISO] Não foi possível atualizar o Kanban local: {ex}", Colors.YELLOW)

    if args.json:
        print(json.dumps(task_request, indent=2, ensure_ascii=False))
        return 0

    print()
    print_color(f"Tarefa {task_id} inicializada com sucesso!", Colors.CYAN)
    print(f"Repositório: {args.repo}")
    print(f"Workflow sugerido: {workflow}")
    print(f"Branch configurada: {branch_name}")
    print_color("Pronto para análise e planejamento.", Colors.GREEN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
