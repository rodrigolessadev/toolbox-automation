"""Script CLI para geração (scaffolding) de novos projetos no padrão Material Design 3.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

TEMPLATE_CHOICES = {
    "react-m3": "web-react-m3",
    "web-react-m3": "web-react-m3",
    "streamlit-m3": "data-app-streamlit-m3",
    "data-app-streamlit-m3": "data-app-streamlit-m3"
}


def scaffold_project(template_type: str, project_name: str, output_dir: Path) -> Path:
    """Gera uma nova estrutura de projeto baseada em um dos templates M3."""
    if template_type not in TEMPLATE_CHOICES:
        raise ValueError(f"Tipo de template desconhecido: '{template_type}'. Opções: {list(TEMPLATE_CHOICES.keys())}")

    src_template = TEMPLATES_DIR / TEMPLATE_CHOICES[template_type]
    if not src_template.exists():
        raise FileNotFoundError(f"Template não encontrado no caminho: {src_template}")

    dest_dir = output_dir / project_name
    if dest_dir.exists():
        raise FileExistsError(f"Diretório de destino já existe: {dest_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copia os arquivos do template
    for root, dirs, files in os.walk(src_template):
        rel_path = Path(root).relative_to(src_template)
        target_sub = dest_dir / rel_path
        target_sub.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            src_file = Path(root) / file_name
            dst_file = target_sub / file_name

            # Substituição de placeholders em arquivos de texto
            try:
                content = src_file.read_text(encoding="utf-8")
                content = content.replace("{{PROJECT_NAME}}", project_name)
                dst_file.write_text(content, encoding="utf-8")
            except UnicodeDecodeError:
                shutil.copy2(src_file, dst_file)

    print(f"✔ [SCAFFOLD] Projeto '{project_name}' criado com sucesso em: {dest_dir}")
    print(f"  Tipo: {template_type} (Material Design 3)")
    return dest_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Toolbox M3 Project Scaffolder")
    parser.add_argument("--type", "-t", required=True, choices=list(TEMPLATE_CHOICES.keys()), help="Tipo de projeto M3")
    parser.add_argument("--name", "-n", required=True, help="Nome do projeto")
    parser.add_argument("--output", "-o", default=".", help="Diretório onde o projeto será gerado")

    args = parser.parse_args()
    try:
        scaffold_project(args.type, args.name, Path(args.output).resolve())
        return 0
    except Exception as err:
        print(f"✖ [ERRO] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
