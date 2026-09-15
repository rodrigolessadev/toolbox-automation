#!/usr/bin/env python3
"""
common_utils.py - Utilitários compartilhados de automação para o ecossistema Toolbox.
Fornece resolução dinâmica de caminhos, execução de comandos do sistema e formatação.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_color(message: str, color: str = Colors.RESET, end: str = "\n", flush: bool = False) -> None:
    """Imprime mensagem colorida no terminal se stdout for TTY ou suportar ANSI."""
    if sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1":
        print(f"{color}{message}{Colors.RESET}", end=end, flush=flush)
    else:
        print(message, end=end, flush=flush)


def detect_workspace_root() -> Path:
    """
    Detecta a raiz do monorepo/ecossistema 'toolbox-ecosystem'.
    Procura por variável de ambiente TOOLBOX_WORKSPACE_ROOT ou
    sobe a hierarquia de diretórios a partir do script atual.
    """
    env_root = os.environ.get("TOOLBOX_WORKSPACE_ROOT")
    if env_root:
        candidate = Path(env_root).resolve()
        if candidate.exists() and candidate.is_dir():
            return candidate

    # Inicia a busca a partir deste arquivo (toolbox-automation/scripts/common_utils.py)
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        # Se contiver a pasta toolbox-automation e toolbox ou toolbox-plugins, achamos a raiz
        if (parent / "toolbox-automation").is_dir() and (
            (parent / "toolbox-plugins").is_dir() or (parent / "toolbox").is_dir()
        ):
            return parent
        if parent.name == "toolbox-ecosystem":
            return parent

    # Fallback: diretório pai de toolbox-automation
    for parent in current.parents:
        if parent.name == "toolbox-automation":
            return parent.parent

    return current.parent.parent


def get_project_path(project_name: str) -> Path:
    """Retorna o caminho absoluto para um projeto do ecossistema."""
    root = detect_workspace_root()
    return (root / project_name).resolve()


def get_gh_executable() -> str:
    """Localiza o executável gh no PATH do sistema ou no diretório padrão local."""
    gh_path = shutil.which("gh")
    if gh_path:
        return gh_path

    # Fallback comum para Linux (~/.local/bin/gh)
    local_bin = Path.home() / ".local" / "bin" / "gh"
    if local_bin.is_file() and os.access(local_bin, os.X_OK):
        return str(local_bin)

    return "gh"


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    check: bool = False,
    capture_output: bool = True,
    env: Optional[Dict[str, str]] = None,
) -> subprocess.CompletedProcess:
    """Executa um comando de forma agnóstica a SO, garantindo PATH correto."""
    merged_env = os.environ.copy()
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin not in merged_env.get("PATH", ""):
        merged_env["PATH"] = f"{local_bin}:{merged_env.get('PATH', '')}"

    if env:
        merged_env.update(env)

    # Se o comando iniciar com 'gh', resolver caminho completo se necessário
    if cmd and cmd[0] == "gh":
        cmd = [get_gh_executable()] + cmd[1:]

    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=check,
        capture_output=capture_output,
        text=True,
        env=merged_env,
    )
