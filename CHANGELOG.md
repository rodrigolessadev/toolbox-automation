# Changelog

Todas as mudanças relevantes da plataforma de automação serão registradas neste arquivo.

## Não publicado

### Funcionalidades (Features)
- **Scaffold M3 de Plugins:** Incorporada a vinculação automática da versão na janela via `plugin_dir=PLUGIN_DIR`, inclusão de asset `.ico` padrão na pasta `ui/assets/` para a barra de tarefas do Windows, e classes utilitárias de ícones (`.icon-sm`, `.icon-md`, `.icon-lg`, `.btn-with-icon`) com catálogo expandido de ícones Lucide no template base `plugin-pywebview-m3` (#24).
- **Sincronização com UI Compartilhada:** O comando de scaffolding `scaffold_project.py` agora detecta e copia a versão mais recente de `toolbox-theme.css` e `icons.js` diretamente da fonte mestre em `plugins/shared/ui/` quando o scaffolding é realizado dentro do repositório `toolbox-plugins` (#24).

- Criada a estrutura inicial do repositório.
- Adicionadas configurações dos projetos locais.
- Adicionada documentação inicial.
- Adicionadas regras básicas para ignorar configurações locais e arquivos sensíveis.
- Integradas as diretrizes técnicas das skills `react-best-practices`, `typescript-expert` e `pytest-skill` em regras (`AGENTS.md`), agentes, prompts e workflows.
