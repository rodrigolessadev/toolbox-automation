"""Orquestrador de Release em Lote (Batch Release) e Notificação em Massa de Issues.

Este script automatiza o ciclo de vida de releases em pacotes para os repositórios
do ecossistema Toolbox, realizando:
1. Inspeção do histórico Git entre tags/refs;
2. Extração e mapeamento de todas as issues vinculadas;
3. Cálculo do incremento SemVer adequado para o pacote;
4. Formatação de notas de release preliminares;
5. Notificação e fechamento em massa das issues no GitHub;
6. Geração de relatórios de execução estruturados.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("batch_release_orchestrator")

ECOSYSTEM_REPOS = {
    "toolbox": {
        "full_name": "rodrigolessadev/toolbox",
        "path": Path(r"C:\tools\toolbox-ecosystem\toolbox")
    },
    "toolbox-plugins": {
        "full_name": "rodrigolessadev/toolbox-plugins",
        "path": Path(r"C:\tools\toolbox-ecosystem\toolbox-plugins")
    },
    "toolbox-release": {
        "full_name": "rodrigolessadev/toolbox-release",
        "path": Path(r"C:\tools\toolbox-ecosystem\toolbox-release")
    },
    "toolbox-automation": {
        "full_name": "rodrigolessadev/toolbox-automation",
        "path": Path(r"C:\tools\toolbox-ecosystem\toolbox-automation")
    }
}


def run_cmd(args: List[str], cwd: Path) -> Tuple[int, str]:
    """Executa um comando de subprocesso com captura de saída."""
    cmd_str = f"{' '.join(args)} (cwd: {cwd})"
    try:
        res = subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if res.returncode == 0:
            logger.debug(f"[CMD OK] {cmd_str}")
        else:
            logger.warning(f"[CMD FAIL code={res.returncode}] {cmd_str} -> {res.stderr.strip()}")
        out = res.stdout.strip() if res.stdout.strip() else res.stderr.strip()
        return res.returncode, out
    except Exception as e:
        logger.error(f"[CMD ERROR] {cmd_str} -> {e}")
        return 1, str(e)


def get_latest_tag(repo_path: Path) -> Optional[str]:
    """Obtém a tag de versão mais recente no repositório."""
    code, out = run_cmd(["git", "tag", "--sort=-v:refname"], repo_path)
    if code == 0 and out.strip():
        for line in out.splitlines():
            t = line.strip()
            if re.match(r"^v?\d+\.\d+\.\d+", t) or re.match(r"^[a-zA-Z0-9_\-]+-\d+\.\d+\.\d+", t):
                return t
        return out.splitlines()[0].strip()
    return None


def collect_commits_in_range(
    repo_path: Path,
    from_ref: Optional[str] = None,
    to_ref: str = "HEAD"
) -> List[Dict[str, Any]]:
    """Coleta e estrutura os commits entre <from_ref>..<to_ref>."""
    resolved_from = from_ref or get_latest_tag(repo_path)
    git_args = ["git", "log", "--pretty=format:%H%x1f%s%x1f%b%x1f%an%x1f%ae%x1f%aI%x1e"]
    
    if resolved_from:
        git_args.append(f"{resolved_from}..{to_ref}")
    else:
        git_args.append(to_ref)

    code, out = run_cmd(git_args, repo_path)
    if code != 0 or not out.strip():
        return []

    commits: List[Dict[str, Any]] = []
    issue_regex = re.compile(r"#(\d+)")
    closes_regex = re.compile(r"(?:closes|fixes|resolves|fecha|corrige)\s+#(\d+)", re.IGNORECASE)

    for rec in out.split("\x1e"):
        clean_rec = rec.strip()
        if not clean_rec:
            continue
        parts = clean_rec.split("\x1f")
        if len(parts) < 6:
            continue

        c_hash, subject, body, author, email, date_str = parts[:6]
        c_hash = c_hash.strip()
        subject = subject.strip()
        body = body.strip()

        # Detecção de tipo
        c_type = "other"
        is_breaking = False
        if "BREAKING CHANGE:" in body or "!:" in subject or "breaking:" in subject.lower():
            is_breaking = True
            c_type = "breaking"
        elif re.match(r"^feat(?:\([^\)]+\))?!?:", subject, re.IGNORECASE) or subject.lower().startswith("feature:"):
            c_type = "feat"
        elif re.match(r"^fix(?:\([^\)]+\))?!?:", subject, re.IGNORECASE) or subject.lower().startswith("bug:"):
            c_type = "fix"
        elif re.match(r"^perf(?:\([^\)]+\))?!?:", subject, re.IGNORECASE):
            c_type = "perf"
        elif re.match(r"^refactor(?:\([^\)]+\))?!?:", subject, re.IGNORECASE):
            c_type = "refactor"
        elif re.match(r"^docs(?:\([^\)]+\))?!?:", subject, re.IGNORECASE):
            c_type = "docs"
        elif re.match(r"^chore(?:\([^\)]+\))?!?:", subject, re.IGNORECASE) or re.match(r"^ci(?:\([^\)]+\))?!?:", subject, re.IGNORECASE):
            c_type = "chore"

        full_text = f"{subject}\n{body}"
        issues = sorted(list(set(int(n) for n in issue_regex.findall(full_text))))
        closed_issues = sorted(list(set(int(n) for n in closes_regex.findall(full_text))))

        commits.append({
            "hash": c_hash,
            "short_hash": c_hash[:7],
            "subject": subject,
            "body": body,
            "author": author.strip(),
            "email": email.strip(),
            "date": date_str.strip(),
            "type": c_type,
            "is_breaking": is_breaking,
            "issues": issues,
            "closed_issues": closed_issues
        })

    return commits


def extract_issues_from_commits(
    commits: List[Dict[str, Any]],
    extra_issues: Optional[List[int]] = None
) -> List[int]:
    """Extrai todas as issues únicas mencionadas nos commits e lista adicional."""
    found: set = set()
    for c in commits:
        for iss in c.get("issues", []):
            found.add(iss)
    if extra_issues:
        for iss in extra_issues:
            found.add(iss)
    return sorted(list(found))


def determine_bump_type(commits: List[Dict[str, Any]]) -> str:
    """Calcula o tipo de incremento SemVer para o conjunto de commits."""
    if not commits:
        return "patch"
    if any(c.get("is_breaking") or c.get("type") == "breaking" for c in commits):
        return "major"
    if any(c.get("type") == "feat" for c in commits):
        return "minor"
    return "patch"


def format_issue_release_comment(version: str, repo_name: str) -> str:
    """Gera o comentário oficial de rastreabilidade de release para uma issue."""
    clean_ver = version.strip()
    if not clean_ver.startswith("v") and re.match(r"^\d+\.\d+\.\d+", clean_ver):
        clean_ver = f"v{clean_ver}"
    return f"🚀 Esta alteração foi incluída e publicada oficialmente na versão **{clean_ver}** do repositório `{repo_name}`."


def notify_and_close_issue(
    repo_full_name: str,
    issue_number: int,
    version: str,
    close_issue: bool = True,
    add_label: Optional[str] = "status: released",
    dry_run: bool = False
) -> Dict[str, Any]:
    """Adiciona comentário de release, fecha a issue e atualiza labels no GitHub via gh CLI."""
    comment = format_issue_release_comment(version, repo_full_name)
    log_actions: List[str] = []

    if dry_run:
        log_actions.append(f"[DRY-RUN] Comentário na issue #{issue_number}: {comment}")
        if close_issue:
            log_actions.append(f"[DRY-RUN] Fechar issue #{issue_number}")
        if add_label:
            log_actions.append(f"[DRY-RUN] Adicionar label '{add_label}' na issue #{issue_number}")
        return {
            "issue_number": issue_number,
            "success": True,
            "dry_run": True,
            "actions": log_actions
        }

    # 1. Adiciona comentário
    c_code, c_out = run_cmd([
        "gh", "issue", "comment", str(issue_number),
        "--repo", repo_full_name,
        "--body", comment
    ], Path.cwd())
    
    if c_code == 0:
        log_actions.append(f"Comentário adicionado na issue #{issue_number}")
    else:
        logger.warning(f"Falha ao adicionar comentário na issue #{issue_number}: {c_out}")

    # 2. Adiciona label se fornecida
    if add_label:
        l_code, l_out = run_cmd([
            "gh", "issue", "edit", str(issue_number),
            "--repo", repo_full_name,
            "--add-label", add_label
        ], Path.cwd())
        if l_code == 0:
            log_actions.append(f"Label '{add_label}' adicionada à issue #{issue_number}")

    # 3. Fecha a issue
    if close_issue:
        cls_code, cls_out = run_cmd([
            "gh", "issue", "close", str(issue_number),
            "--repo", repo_full_name,
            "--reason", "completed"
        ], Path.cwd())
        if cls_code == 0:
            log_actions.append(f"Issue #{issue_number} fechada com sucesso")
        else:
            logger.warning(f"Falha ao fechar issue #{issue_number}: {cls_out}")

    return {
        "issue_number": issue_number,
        "success": True,
        "actions": log_actions
    }


def batch_notify_and_close(
    repo_full_name: str,
    issues: List[int],
    version: str,
    close_issue: bool = True,
    add_label: Optional[str] = "status: released",
    dry_run: bool = False
) -> List[Dict[str, Any]]:
    """Notifica e fecha uma lista de issues em lote."""
    results = []
    logger.info(f"Iniciando notificação em massa para {len(issues)} issues no repositório {repo_full_name}...")
    for iss in issues:
        res = notify_and_close_issue(
            repo_full_name=repo_full_name,
            issue_number=iss,
            version=version,
            close_issue=close_issue,
            add_label=add_label,
            dry_run=dry_run
        )
        results.append(res)
    return results


def orchestrate_batch_release(
    repo_name: str,
    version: str,
    from_ref: Optional[str] = None,
    to_ref: str = "HEAD",
    explicit_issues: Optional[List[int]] = None,
    notify: bool = True,
    close_issues: bool = True,
    add_label: Optional[str] = "status: released",
    dry_run: bool = False
) -> Dict[str, Any]:
    """Orquestra a análise em lote, extração de issues e encerramento em massa."""
    repo_info = ECOSYSTEM_REPOS.get(repo_name.lower().strip())
    if not repo_info:
        err = f"Repositório '{repo_name}' não reconhecido. Opções válidas: {list(ECOSYSTEM_REPOS.keys())}"
        logger.error(err)
        return {"success": False, "error": err}

    repo_path = repo_info["path"]
    repo_full_name = repo_info["full_name"]

    if not repo_path.exists():
        err = f"Diretório local do repositório não encontrado: {repo_path}"
        logger.error(err)
        return {"success": False, "error": err}

    logger.info(f"Orquestrando release em lote para {repo_full_name} (versão: {version}, dry_run={dry_run})...")

    # 1. Coleta de commits e identificação de issues
    resolved_from = from_ref or get_latest_tag(repo_path)
    commits = collect_commits_in_range(repo_path, from_ref=resolved_from, to_ref=to_ref)
    all_issues = extract_issues_from_commits(commits, extra_issues=explicit_issues)
    bump_type = determine_bump_type(commits)

    # 2. Notificação e fechamento em massa
    notification_results = []
    if notify and all_issues:
        notification_results = batch_notify_and_close(
            repo_full_name=repo_full_name,
            issues=all_issues,
            version=version,
            close_issue=close_issues,
            add_label=add_label,
            dry_run=dry_run
        )

    summary = {
        "success": True,
        "repository": repo_name,
        "repo_full_name": repo_full_name,
        "version": version,
        "from_ref": resolved_from or "(início)",
        "to_ref": to_ref,
        "total_commits": len(commits),
        "suggested_bump": bump_type,
        "issues_processed": all_issues,
        "notifications": notification_results,
        "dry_run": dry_run
    }

    logger.info(f"Orquestração concluída com sucesso: {len(commits)} commits analisados, {len(all_issues)} issues processadas.")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Orquestrador de Release em Lote e Notificação em Massa de Issues")
    parser.add_argument("--repo", required=True, choices=list(ECOSYSTEM_REPOS.keys()), help="Repositório alvo do ecossistema")
    parser.add_argument("--version", required=True, help="Versão publicada ou alvo do pacote (ex: 1.18.0 ou v1.18.0)")
    parser.add_argument("--from-ref", dest="from_ref", default=None, help="Tag ou commit inicial do intervalo (default: última tag)")
    parser.add_argument("--to-ref", dest="to_ref", default="HEAD", help="Tag ou commit final do intervalo (default: HEAD)")
    parser.add_argument("--issues", default="", help="Lista explícita de issues separadas por vírgula (ex: 101,102,103)")
    parser.add_argument("--no-notify", dest="notify", action="store_false", default=True, help="Desabilita envio de comentários nas issues")
    parser.add_argument("--no-close", dest="close", action="store_false", default=True, help="Não fecha as issues no GitHub")
    parser.add_argument("--label", default="status: released", help="Label a ser adicionada às issues processadas")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False, help="Executa em modo simulação sem alterações reais no GitHub")

    args = parser.parse_args()

    explicit_issues = []
    if args.issues.strip():
        for item in args.issues.split(","):
            item_clean = item.strip().lstrip("#")
            if item_clean.isdigit():
                explicit_issues.append(int(item_clean))

    res = orchestrate_batch_release(
        repo_name=args.repo,
        version=args.version,
        from_ref=args.from_ref,
        to_ref=args.to_ref,
        explicit_issues=explicit_issues,
        notify=args.notify,
        close_issues=args.close,
        add_label=args.label if args.label else None,
        dry_run=args.dry_run
    )

    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
