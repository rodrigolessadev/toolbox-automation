#!/usr/bin/env python3
"""
start_task.py - Inicializa uma tarefa de automação criando um checkpoint persistente.
Substitui o script legado start-task.ps1 de forma multiplataforma.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any, Dict

from common_utils import Colors, print_color


def create_task_checkpoint(
    task_id: str,
    description: str,
    checkpoints_dir: Path,
    metadata: Dict[str, Any] | None = None,
) -> Path:
    """Cria e salva um arquivo de checkpoint para uma tarefa."""
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_file = checkpoints_dir / f"{task_id}.json"

    data: Dict[str, Any] = {
        "task_id": task_id,
        "description": description,
        "status": "in_progress",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "current_phase": "analysis",
        "blocked": False,
    }
    if metadata:
        data.update(metadata)

    checkpoint_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return checkpoint_file


def main() -> int:
    now_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    default_id = f"TASK-{now_str}"

    parser = argparse.ArgumentParser(description="Inicializa uma tarefa de automação e registra checkpoint.")
    parser.add_argument("--task-id", default=default_id, help=f"Identificador da tarefa (padrão: {default_id})")
    parser.add_argument("--description", default="Nova tarefa de automação", help="Descrição resumida da tarefa")
    parser.add_argument("--dir", default=".agent/checkpoints", help="Diretório de armazenamento dos checkpoints")
    parser.add_argument("--json", action="store_true", help="Imprime o checkpoint gerado em JSON")
    args = parser.parse_args()

    checkpoints_dir = Path(args.dir)
    print_color(f"Inicializando tarefa: {args.task_id}...", Colors.CYAN)

    checkpoint_path = create_task_checkpoint(
        task_id=args.task_id,
        description=args.description,
        checkpoints_dir=checkpoints_dir,
    )

    if args.json:
        print(checkpoint_path.read_text(encoding="utf-8"))
        return 0

    print_color(f"Checkpoint inicial criado em: {checkpoint_path}", Colors.GREEN)
    print_color(f"Tarefa {args.task_id} iniciada com sucesso.", Colors.GREEN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
