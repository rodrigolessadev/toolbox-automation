"""Script CLI para geração (scaffolding) de novos projetos no padrão Material Design 3.
Suporta aplicações React, Streamlit e plugins oficiais pywebview para o ecossistema Toolbox.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

TEMPLATE_CHOICES: Dict[str, str] = {
    "react-m3": "web-react-m3",
    "web-react-m3": "web-react-m3",
    "streamlit-m3": "data-app-streamlit-m3",
    "data-app-streamlit-m3": "data-app-streamlit-m3",
    "plugin-pywebview": "plugin-pywebview-m3",
    "pywebview-m3": "plugin-pywebview-m3",
}


def sanitize_plugin_id(raw_id: str) -> str:
    """Sanitiza e padroniza identificador de plugin em formato kebab-case."""
    clean = raw_id.lower().strip().replace(" ", "-").replace("_", "-")
    clean = re.sub(r"[^a-z0-9\-]", "", clean)
    clean = re.sub(r"-+", "-", clean).strip("-")
    return clean or "novo-plugin"


def to_pascal_case(kebab_str: str) -> str:
    """Converte string kebab-case em PascalCase para classes e identificadores Python."""
    parts = re.split(r"[^a-zA-Z0-9]", kebab_str)
    return "".join(p.capitalize() for p in parts if p) or "NovoPlugin"


def scaffold_project(
    template_type: str,
    project_name: str,
    output_dir: Path,
    plugin_id: Optional[str] = None,
    plugin_icon: Optional[str] = None,
    plugin_description: Optional[str] = None,
    test_output_dir: Optional[Path] = None,
) -> Path:
    """Gera uma nova estrutura de projeto ou plugin baseada em um dos templates M3."""
    if template_type not in TEMPLATE_CHOICES:
        raise ValueError(f"Tipo de template desconhecido: '{template_type}'. Opções: {list(TEMPLATE_CHOICES.keys())}")

    src_template = TEMPLATES_DIR / TEMPLATE_CHOICES[template_type]
    if not src_template.exists():
        raise FileNotFoundError(f"Template não encontrado no caminho: {src_template}")

    is_plugin = "pywebview" in template_type

    # Resolução de nomes e IDs
    clean_id = sanitize_plugin_id(plugin_id or project_name)
    pascal_name = to_pascal_case(clean_id)
    upper_id = clean_id.upper().replace("-", "_")
    icon = plugin_icon or ("check-square" if "tarefa" in clean_id else "box")
    desc = plugin_description or f"Plugin oficial {project_name} para o ecossistema Toolbox."

    folder_name = clean_id if is_plugin else project_name
    dest_dir = output_dir / folder_name

    if dest_dir.exists():
        raise FileExistsError(f"Diretório de destino já existe: {dest_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PLUGIN_NAME}}": project_name,
        "{{PLUGIN_ID}}": clean_id,
        "{{PLUGIN_ID_UPPER}}": upper_id,
        "{{PLUGIN_NAME_PASCAL}}": pascal_name,
        "{{PLUGIN_ICON}}": icon,
        "{{PLUGIN_DESCRIPTION}}": desc,
    }

    test_template_content = None

    # Copia os arquivos do template aplicando substituições
    for root, dirs, files in os.walk(src_template):
        rel_path = Path(root).relative_to(src_template)
        target_sub = dest_dir / rel_path
        target_sub.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            src_file = Path(root) / file_name

            # Trata template de teste separadamente para gravação posterior
            if file_name == "test_plugin.py.template":
                try:
                    raw_test = src_file.read_text(encoding="utf-8")
                    for k, v in replacements.items():
                        raw_test = raw_test.replace(k, str(v))
                    test_template_content = raw_test
                except Exception:
                    pass
                continue

            dst_file = target_sub / file_name

            try:
                content = src_file.read_text(encoding="utf-8")
                for k, v in replacements.items():
                    content = content.replace(k, str(v))
                dst_file.write_text(content, encoding="utf-8")
            except UnicodeDecodeError:
                shutil.copy2(src_file, dst_file)

    # Geração do arquivo de testes para plugins
    if is_plugin and test_template_content:
        # Determina onde gravar o teste unitário gerado
        target_test_dir = test_output_dir
        if not target_test_dir:
            # Tenta encontrar pasta tests paralela se o output for uma pasta de plugins
            candidate = dest_dir.parent.parent / "tests"
            if candidate.exists() and candidate.is_dir():
                target_test_dir = candidate
            else:
                target_test_dir = dest_dir / "tests"

        target_test_dir.mkdir(parents=True, exist_ok=True)
        test_file = target_test_dir / f"test_plugin_{clean_id.replace('-', '_')}.py"
        test_file.write_text(test_template_content, encoding="utf-8")
        print(f"✔ [TEST] Arquivo de teste gerado: {test_file}")

    print(f"✔ [SCAFFOLD] Estrutura criada com sucesso em: {dest_dir}")
    print(f"  Tipo: {template_type} (Material Design 3)")
    if is_plugin:
        print(f"  Plugin ID: {clean_id} | Ícone: {icon}")

    return dest_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Toolbox M3 Project and Plugin Scaffolder")
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=list(TEMPLATE_CHOICES.keys()),
        help="Tipo de template a gerar (ex: plugin-pywebview, react-m3, streamlit-m3)"
    )
    parser.add_argument("--name", "-n", required=True, help="Nome amigável de exibição (ex: 'Calculadora de Horas')")
    parser.add_argument("--output", "-o", default=".", help="Diretório onde o projeto/plugin será gerado")
    parser.add_argument("--id", help="Identificador único kebab-case do plugin (ex: 'calc-horas'). Se omitido, deriva de --name.")
    parser.add_argument("--icon", default="box", help="Ícone oficial Lucide (ex: 'check-square', 'clock', 'box')")
    parser.add_argument("--description", help="Descrição sucinta das funcionalidades do plugin")
    parser.add_argument("--test-output", help="Diretório opcional para gravação do arquivo de testes unitários")

    args = parser.parse_args()
    try:
        scaffold_project(
            template_type=args.type,
            project_name=args.name,
            output_dir=Path(args.output).resolve(),
            plugin_id=args.id,
            plugin_icon=args.icon,
            plugin_description=args.description,
            test_output_dir=Path(args.test_output).resolve() if args.test_output else None,
        )
        return 0
    except Exception as err:
        print(f"✖ [ERRO] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
