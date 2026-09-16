# Changelog

Todas as mudanças relevantes da plataforma de automação serão registradas neste arquivo.

## Não publicado

### Funcionalidades (Features)
- **Scaffold M3 de Plugins:** Incorporada a vinculação automática da versão na janela via `plugin_dir=PLUGIN_DIR`, inclusão de asset `.ico` padrão na pasta `ui/assets/` para a barra de tarefas do Windows, e classes utilitárias de ícones (`.icon-sm`, `.icon-md`, `.icon-lg`, `.btn-with-icon`) com catálogo expandido de ícones Lucide no template base `plugin-pywebview-m3` (#24).
- **Sincronização com UI Compartilhada:** O comando de scaffolding `scaffold_project.py` agora detecta e copia a versão mais recente de `toolbox-theme.css` e `icons.js` diretamente da fonte mestre em `plugins/shared/ui/` quando o scaffolding é realizado dentro do repositório `toolbox-plugins` (#24).
- **Auditoria de Conformidade de Plugins (5 Regras & Shared UI):** Reformulado o script `audit_plugins_compliance.py` e integrado o comando `tb_auto audit-plugins` para validar rigorosamente as 5 regras de identidade e UX (ícone no manifesto, taskbar .ico, versão na janela, classes utilitárias de ícones e tema claro M3), além de verificação de paridade por hash SHA-256 contra a fonte mestre `plugins/shared/ui/` (#25).
- **Sincronização de UI Compartilhada (`tb_auto sync-ui`):** Criado o script `sync_plugins_ui.py` e integrado o comando `tb_auto sync-ui` para propagar automaticamente as fontes mestre de UI (`toolbox-theme.css` e `icons.js`) de `plugins/shared/ui/` para todos os plugins em `toolbox-plugins/plugins/`, com suporte a verificação sem alteração (`--check` / `--dry-run`), sincronização direcionada (`--plugin <id>`), saída estruturada (`--json`), verificação de integridade via hash SHA-256 e tempo de execução sub-segundo (#26).

- Criada a estrutura inicial do repositório.
- Adicionadas configurações dos projetos locais.
- Adicionada documentação inicial.
- Adicionadas regras básicas para ignorar configurações locais e arquivos sensíveis.
- Integradas as diretrizes técnicas das skills `react-best-practices`, `typescript-expert` e `pytest-skill` em regras (`AGENTS.md`), agentes, prompts e workflows.
