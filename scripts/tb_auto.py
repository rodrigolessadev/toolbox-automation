#!/usr/bin/env python3
"""
tb_auto.py - Ponto de Entrada Unificado da CLI de Automação do Toolbox Ecosystem.
Agrega todos os utilitários operacionais em comandos e subcomandos intuitivos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="tb_auto.py",
        description="Toolbox Automation CLI - Ferramentas operacionais multiplataforma para o ecossistema Toolbox.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # 1. check
    check_p = subparsers.add_parser("check", help="Verifica a integridade dos projetos locais")
    check_p.add_argument("--root", help="Caminho explícito da raiz do workspace")
    check_p.add_argument("--json", action="store_true", help="Retorna em formato JSON")

    # 2. issues
    issues_p = subparsers.add_parser("issues", help="Consulta issues abertas nos projetos")
    issues_p.add_argument(
        "--project",
        choices=["all", "toolbox", "toolbox-plugins", "toolbox-automation", "toolbox-release"],
        default="all",
        help="Projeto específico ou 'all'",
    )
    issues_p.add_argument("--owner", default="rodrigolessadev", help="Proprietário no GitHub")
    issues_p.add_argument("--json", action="store_true", help="Retorna em formato JSON")

    # 3. init-task
    init_p = subparsers.add_parser("init-task", help="Inicializa uma tarefa a partir de uma issue")
    init_p.add_argument("--repo", required=True, choices=["toolbox", "toolbox-plugins", "toolbox-automation", "toolbox-release"])
    init_p.add_argument("--issue", type=int, required=True, help="Número da issue")
    init_p.add_argument("--owner", default="rodrigolessadev")
    init_p.add_argument("--no-branch", action="store_true", help="Não cria branch git local")
    init_p.add_argument("--json", action="store_true")

    # 4. task
    task_p = subparsers.add_parser("task", help="Gerencia checkpoints de tarefas")
    task_sub = task_p.add_subparsers(dest="task_action", help="Ação de tarefa")

    task_start = task_sub.add_parser("start", help="Cria um novo checkpoint de tarefa")
    task_start.add_argument("--task-id", help="Identificador único da tarefa")
    task_start.add_argument("--description", default="Nova tarefa de automação")
    task_start.add_argument("--dir", default=".agent/checkpoints")
    task_start.add_argument("--json", action="store_true")

    task_resume = task_sub.add_parser("resume", help="Inspeciona e retoma uma tarefa")
    task_resume.add_argument("task_id", help="Identificador único da tarefa")
    task_resume.add_argument("--dir", default=".agent/checkpoints")
    task_resume.add_argument("--json", action="store_true")

    # 5. context
    ctx_p = subparsers.add_parser("context", help="Valida arquivos de contexto persistente (.agent)")
    ctx_p.add_argument("--dir", default=".agent", help="Diretório de contexto")
    ctx_p.add_argument("--with-graph", action="store_true", help="Checa também o grafo do Graphify")
    ctx_p.add_argument("--json", action="store_true")

    # 6. graph
    graph_p = subparsers.add_parser("graph", help="Governança segura e análise de impacto do Graphify")
    graph_p.add_argument("--build-graph", action="store_true", help="Gera grafo seguro")
    graph_p.add_argument("--impact-analysis", action="store_true", help="Análise de impacto somente leitura")
    graph_p.add_argument("--target-file", help="Arquivo alvo para análise")
    graph_p.add_argument("--json", action="store_true")

    # 7. scaffold
    scaffold_p = subparsers.add_parser("scaffold", help="Cria novo projeto ou plugin a partir de templates oficiais")
    scaffold_p.add_argument("name", help="Nome do projeto/plugin")
    scaffold_p.add_argument(
        "--type",
        choices=["react-m3", "data-app-streamlit-m3", "plugin-pywebview"],
        default="plugin-pywebview",
        help="Tipo de template a ser gerado",
    )
    scaffold_p.add_argument("--dest", help="Diretório de destino")
    scaffold_p.add_argument("--title", help="Título amigável para exibição")
    scaffold_p.add_argument("--desc", help="Descrição sucinta")
    scaffold_p.add_argument("--icon", default="box", help="Identificador do ícone Lucide")

    # 8. search (Code Search via AST / ast-grep)
    search_p = subparsers.add_parser("search", help="Busca estrutural de classes, funções e imports (AST / ast-grep)")
    search_p.add_argument("--symbol", default="*", help="Nome ou fragmento do símbolo")
    search_p.add_argument("--type", choices=["all", "class", "func", "import"], default="all", help="Tipo de símbolo")
    search_p.add_argument("--path", default=None, help="Caminho alvo para busca")
    search_p.add_argument("--pattern", default=None, help="Padrão estrutural do ast-grep")
    search_p.add_argument("--json", action="store_true", help="Retorna em formato JSON")

    # 9. pack (Context Pack / Repomix)
    pack_p = subparsers.add_parser("pack", help="Empacota cirurgicamente o contexto de um plugin ou diretório (Repomix)")
    pack_p.add_argument("--dir", required=True, help="Diretório alvo a empacotar")
    pack_p.add_argument("--output", default=None, help="Caminho do arquivo Markdown de saída")
    pack_p.add_argument("--max-tokens", type=int, default=32000, help="Limite máximo de tokens")
    # 10. audit-plugins
    audit_p = subparsers.add_parser("audit-plugins", help="Audita conformidade dos plugins (5 regras de UX/UI e sincronização da UI compartilhada)")
    audit_p.add_argument("--root", help="Caminho explícito para a pasta raiz de toolbox-plugins")
    audit_p.add_argument("--plugin", help="Auditar somente um plugin específico")
    audit_p.add_argument("--strict", action="store_true", help="Retorna código de saída 1 em caso de qualquer pendência")
    audit_p.add_argument("--json", action="store_true", help="Retorna resultado estruturado em JSON")

    # 11. sync-ui
    sync_p = subparsers.add_parser("sync-ui", help="Sincroniza folhas de estilo e ícones da fonte mestre (shared/ui/) para os plugins")
    sync_p.add_argument("--root", help="Caminho explícito para a pasta raiz de toolbox-plugins")
    sync_p.add_argument("--plugin", help="Sincroniza apenas um plugin específico")
    sync_p.add_argument("--check", "--dry-run", action="store_true", help="Apenas verifica conformidade sem alterar arquivos (exit 1 em divergência)")
    sync_p.add_argument("--verbose", action="store_true", help="Exibe detalhes de todos os arquivos processados")
    sync_p.add_argument("--json", action="store_true", help="Retorna resultado em formato JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    scripts_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(scripts_dir))

    if args.command == "check":
        import check_projects
        sys.argv = ["check_projects.py"]
        if args.root:
            sys.argv.extend(["--root", args.root])
        if args.json:
            sys.argv.append("--json")
        return check_projects.main()

    elif args.command == "issues":
        import get_issues
        sys.argv = ["get_issues.py", "--project", args.project, "--owner", args.owner]
        if args.json:
            sys.argv.append("--json")
        return get_issues.main()

    elif args.command == "init-task":
        import init_task
        sys.argv = ["init_task.py", "--repo", args.repo, "--issue", str(args.issue), "--owner", args.owner]
        if args.no_branch:
            sys.argv.append("--no-branch")
        if args.json:
            sys.argv.append("--json")
        return init_task.main()

    elif args.command == "task":
        if args.task_action == "start":
            import start_task
            sys.argv = ["start_task.py", "--dir", args.dir]
            if args.task_id:
                sys.argv.extend(["--task-id", args.task_id])
            if args.description:
                sys.argv.extend(["--description", args.description])
            if args.json:
                sys.argv.append("--json")
            return start_task.main()
        elif args.task_action == "resume":
            import resume_task
            sys.argv = ["resume_task.py", args.task_id, "--dir", args.dir]
            if args.json:
                sys.argv.append("--json")
            return resume_task.main()
        else:
            task_p.print_help()
            return 0

    elif args.command == "context":
        import load_context
        sys.argv = ["load_context.py", "--dir", args.dir]
        if args.with_graph:
            sys.argv.append("--with-graph")
        if args.json:
            sys.argv.append("--json")
        return load_context.main()

    elif args.command == "graph":
        import update_graph
        sys.argv = ["update_graph.py"]
        if args.build_graph:
            sys.argv.append("--build-graph")
        if args.impact_analysis:
            sys.argv.append("--impact-analysis")
        if args.target_file:
            sys.argv.extend(["--target-file", args.target_file])
        if args.json:
            sys.argv.append("--json")
        return update_graph.main()

    elif args.command == "scaffold":
        import scaffold_project
        sys.argv = ["scaffold_project.py", args.name, "--type", args.type]
        if args.dest:
            sys.argv.extend(["--dest", args.dest])
        if args.title:
            sys.argv.extend(["--title", args.title])
        if args.desc:
            sys.argv.extend(["--desc", args.desc])
        if args.icon:
            sys.argv.extend(["--icon", args.icon])
        return scaffold_project.main()

    elif args.command == "search":
        import code_search
        sys.argv = ["code_search.py", "--symbol", args.symbol, "--type", args.type]
        if args.path:
            sys.argv.extend(["--path", args.path])
        if args.pattern:
            sys.argv.extend(["--pattern", args.pattern])
        if args.json:
            sys.argv.append("--json")
        return code_search.main()

    elif args.command == "pack":
        import pack_context
        sys.argv = ["pack_context.py", "--dir", args.dir, "--max-tokens", str(args.max_tokens)]
        if args.output:
            sys.argv.extend(["--output", args.output])
        if args.json:
            sys.argv.append("--json")
        return pack_context.main()

    elif args.command == "audit-plugins":
        import audit_plugins_compliance
        argv = []
        if args.root:
            argv.extend(["--root", args.root])
        if args.plugin:
            argv.extend(["--plugin", args.plugin])
        if args.strict:
            argv.append("--strict")
        if args.json:
            argv.append("--json")
        return audit_plugins_compliance.main(argv)

    elif args.command == "sync-ui":
        import sync_plugins_ui
        argv = []
        if args.root:
            argv.extend(["--root", args.root])
        if args.plugin:
            argv.extend(["--plugin", args.plugin])
        if args.check:
            argv.append("--check")
        if args.verbose:
            argv.append("--verbose")
        if args.json:
            argv.append("--json")
        return sync_plugins_ui.main(argv)

    return 0


if __name__ == "__main__":
    sys.exit(main())
