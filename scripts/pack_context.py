#!/usr/bin/env python3
"""
pack_context.py - Empacota cirurgicamente o contexto de um plugin ou diretório para agentes de IA.
Inspirado no Repomix (Repopack), gera árvore de arquivos, conteúdo consolidado e estimativa de tokens.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from common_utils import Colors, print_color


IGNORED_DIRS: Set[str] = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "coverage",
    ".vscode",
    ".idea",
    "graphify-out",
}

IGNORED_EXTENSIONS: Set[str] = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".zip",
    ".tar",
    ".gz",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".db",
    ".sqlite",
    ".sqlite3",
}


def estimate_tokens(text: str) -> int:
    """Calcula estimativa aproximada de tokens (média de 4 caracteres por token)."""
    return max(1, len(text) // 4)


def build_directory_tree(dir_path: Path, prefix: str = "") -> str:
    """Gera uma representação textual da árvore de diretórios."""
    lines: List[str] = []
    try:
        entries = sorted(
            [e for e in dir_path.iterdir() if e.name not in IGNORED_DIRS and e.suffix not in IGNORED_EXTENSIONS],
            key=lambda x: (not x.is_dir(), x.name.lower()),
        )
    except PermissionError:
        return f"{prefix}[Permissão negada]\n"

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{entry.name}{'/' if entry.is_dir() else ''}")

        if entry.is_dir():
            sub_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
            lines.append(build_directory_tree(entry, sub_prefix))

    return "\n".join(filter(None, lines))


def pack_directory(
    target_dir: Path,
    include_extensions: Optional[List[str]] = None,
) -> Tuple[str, Dict[str, Any]]:
    """Empacota os arquivos de código e texto do diretório alvo."""
    packed_files: List[Dict[str, Any]] = []
    total_bytes = 0

    tree_str = f"{target_dir.name}/\n" + build_directory_tree(target_dir)

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            file_path = Path(root) / f
            if file_path.suffix.lower() in IGNORED_EXTENSIONS:
                continue

            if include_extensions and file_path.suffix.lower() not in include_extensions:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            rel_path = file_path.relative_to(target_dir)
            total_bytes += len(content.encode("utf-8"))
            packed_files.append({
                "path": str(rel_path),
                "extension": file_path.suffix,
                "size_bytes": len(content.encode("utf-8")),
                "tokens_est": estimate_tokens(content),
                "content": content,
            })

    packed_files.sort(key=lambda x: x["path"])

    # Monta documento Markdown consolidado
    md_parts: List[str] = [
        f"# Context Pack: `{target_dir.name}`",
        f"\n**Gerado em:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
        f"**Diretório Alvo:** `{target_dir.resolve()}`",
        f"**Total de Arquivos:** {len(packed_files)}",
        f"**Tamanho Total:** {total_bytes / 1024:.1f} KB",
        "\n## 📂 Árvore de Arquivos\n",
        "```text",
        tree_str,
        "```",
        "\n## 📄 Conteúdo dos Arquivos\n",
    ]

    for item in packed_files:
        ext = item["extension"].lstrip(".") or "text"
        md_parts.append(f"### File: `{item['path']}` (Tokens est: ~{item['tokens_est']})\n")
        md_parts.append(f"```{ext}")
        md_parts.append(item["content"].rstrip())
        md_parts.append("```\n")

    full_markdown = "\n".join(md_parts)
    total_tokens = estimate_tokens(full_markdown)

    meta = {
        "target_dir": str(target_dir.resolve()),
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_files": len(packed_files),
        "total_bytes": total_bytes,
        "estimated_tokens": total_tokens,
        "files_summary": [
            {"path": f["path"], "tokens": f["tokens_est"], "size": f["size_bytes"]}
            for f in packed_files
        ],
    }

    return full_markdown, meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Empacota cirurgicamente o contexto de um plugin ou diretório.")
    parser.add_argument("--dir", required=True, help="Diretório alvo a ser empacotado")
    parser.add_argument("--output", default=None, help="Caminho do arquivo Markdown de saída (opcional)")
    parser.add_argument("--max-tokens", type=int, default=32000, help="Limite máximo desejado de tokens (alerta)")
    parser.add_argument("--json", action="store_true", help="Retorna apenas metadados em formato JSON")
    args = parser.parse_args()

    target_path = Path(args.dir).resolve()
    if not target_path.exists() or not target_path.is_dir():
        print_color(f"[ERRO] Diretório não encontrado ou inválido: {target_path}", Colors.RED)
        return 1

    markdown_pack, meta = pack_directory(target_path)

    if args.json:
        print(json.dumps(meta, indent=2, ensure_ascii=False))
        return 0

    if args.output:
        out_file = Path(args.output).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(markdown_pack, encoding="utf-8")
        print_color("====================================================", Colors.CYAN)
        print_color(f"  Toolbox Context Pack (Repomix Inspired)           ", Colors.CYAN)
        print_color("====================================================", Colors.CYAN)
        print(f"Diretório: {meta['target_dir']}")
        print(f"Total de Arquivos: {meta['total_files']}")
        print(f"Tamanho: {meta['total_bytes'] / 1024:.1f} KB")
        print(f"Tokens Estimados: ~{meta['estimated_tokens']:,}")
        print_color(f"Pacote gravado com sucesso em: {out_file}", Colors.GREEN)

        if meta["estimated_tokens"] > args.max_tokens:
            print_color(
                f"[AVISO] O pacote excedeu o limite desejado de {args.max_tokens:,} tokens!",
                Colors.YELLOW,
            )
    else:
        print(markdown_pack)

    return 0


if __name__ == "__main__":
    sys.exit(main())
