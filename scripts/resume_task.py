#!/usr/bin/env python3
"""
resume_task.py - Retoma e inspeciona uma tarefa de automação a partir de seu checkpoint.
Substitui o script legado resume-task.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from common_utils import Colors, print_color


def read_task_checkpoint(task_id: str, checkpoints_dir: Path) -> Dict[str, Any]:
    """Lê e retorna o checkpoint de uma tarefa."""
    checkpoint_file = checkpoints_dir / f"{task_id}.json"
    if not checkpoint_file.exists():
        raise FileNotFoundError(f"Checkpoint da tarefa não encontrado: {checkpoint_file}")

    data = json.loads(checkpoint_file.read_text(encoding="utf-8"))
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica e retoma uma tarefa a partir de seu checkpoint.")
    parser.add_argument("task_id", help="Identificador da tarefa a ser retomada (ex: TASK-20260915-180000)")
    parser.add_argument("--dir", default=".agent/checkpoints", help="Diretório de armazenamento dos checkpoints")
    parser.add_argument("--json", action="store_true", help="Imprime o estado do checkpoint em formato JSON")
    args = parser.parse_args()

    checkpoints_dir = Path(args.dir)
    print_color(f"Verificando retomada da tarefa: {args.task_id}...", Colors.CYAN)

    try:
        data = read_task_checkpoint(args.task_id, checkpoints_dir)
    except FileNotFoundError as e:
        print_color(f"[ERRO] {e}", Colors.RED)
        return 1

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    print_color("Tarefa encontrada.", Colors.GREEN)
    print("Status atual: ", end="")
    print_color(data.get("status", "unknown"), Colors.CYAN)
    print("Fase atual: ", end="")
    print_color(data.get("current_phase", "unknown"), Colors.CYAN)

    if data.get("blocked"):
        print_color("[AVISO] Esta tarefa possui bloqueios registrados. Requer análise prévia.", Colors.YELLOW)

    print_color(f"Tarefa {args.task_id} pronta para retomada segura.", Colors.GREEN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
