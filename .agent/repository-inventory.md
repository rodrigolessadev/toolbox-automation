# Inventário dos repositórios

## Data do inventário

- Data: 2026-08-13
- Responsável: Rodrigo
- Status: inicial

## 1. toolbox-automation

- Caminho local: `C:\tools\toolbox-automation`
- Branch atual: main
- Último commit: cbfafc7 (HEAD -> main) chore: criar base da automação do Toolbox
- Estado Git: `?? .agent/` (diretório não rastreado)
- Linguagem principal:
- Ferramentas de validação:
- Diretórios principais:
  - `.agent`
  - `agents`
  - `config`
  - `docs`
  - `evals`
  - `mcp`
  - `policies`
  - `prompts`
  - `schemas`
  - `scripts`
  - `workflows`
- Arquivos de configuração:
- Testes:
- Riscos identificados:
- Pendências:

## 2. toolbox

- Caminho local: C:\tools\toolbox
- Repositório remoto: https://github.com/rodrigolessadev/toolbox
- Branch atual: main
- Último commit: df05eb7 (HEAD -> main, tag: v1.15.0, origin/main, origin/feature/suporte-a-outros-tipos-de-plugis, origin/HEAD, feature/suporte-a-outros-tipos-de-plugis) feat(core): inclui componentes React, protocolo IPC Rust e atualizacoes de plugins na v1.15.0
- Estado Git:
- Linguagem principal: TypeScript e Rust
- Framework ou runtime: Node.js, React e Tauri
- Gerenciador de dependências: npm (package-lock.json) e Cargo
- Ferramenta de build: Vite
- Ferramenta de testes:
- Ferramenta de lint:
- Ferramenta de formatação:
- Ferramenta de empacotamento: Tauri
- Ferramentas de validação:
- Diretórios principais:
  - .agents
  - .claude
  - .code-review-graph
  - .codebuddy
  - .gemini
  - .github
  - .kiro
  - .qoder
  - .release_plugin_state
  - .venv
  - .vscode
  - anotacoes
  - builds
  - commits
  - dist
  - docs
  - graphify-out
  - node_modules
  - plugins
  - releases
  - site
  - src
  - src-tauri
- Arquivos de configuração:
  - package.json
  - package-lock.json
  - vite.config.ts
  - src-tauri/Cargo.toml
  - src-tauri/package.json
  - site/package.json
  - site/package-lock.json
  - site/node_modules/yarn.lock
- Testes:
- Sistema de plugins:
- Riscos identificados:
- Pendências:

### Diretórios principais do repositório toolbox

| Diretório | Finalidade |
|------------|------------|
| .agents | Configurações e artefatos relacionados a agentes de IA |
| .claude | Configurações e instruções para Claude |
| .code-review-graph | Artefatos de análise e revisão de código |
| .codebuddy | Configurações da ferramenta CodeBuddy |
| .gemini | Configurações relacionadas ao Gemini |
| .github | Workflows, templates e configurações do GitHub |
| .kiro | Configurações da ferramenta Kiro |
| .qoder | Configurações da ferramenta Qoder |
| .release_plugin_state | Controle de estado/versionamento de plugins para releases |
| .venv | Ambiente virtual Python |
| .vscode | Configurações do Visual Studio Code |
| anotacoes | Documentação e anotações do projeto |
| builds | Artefatos ou scripts de build |
| commits | Registros e materiais relacionados a commits/releases |
| dist | Artefatos gerados de distribuição |
| docs | Documentação do projeto |
| graphify-out | Saída de ferramentas de análise/grafo |
| node_modules | Dependências Node.js instaladas |
| plugins | Plugins utilizados pelo Toolbox |
| releases | Arquivos relacionados a empacotamento e releases |
| site | Projeto do site/documentação web |
| src | Código-fonte principal da aplicação |
| src-tauri | Código Rust e configuração da aplicação Tauri |

- Diretórios de código:
  - src
  - src/components
  - src/lib
  - src-tauri/src
  - plugins

- Diretórios do site:
  - site/src
  - site/src/components
  - site/src/lib
  - site/src/pages/docs
  - site/public

- Diretórios de documentação:
  - docs

## 3. toolbox-plugins

- Caminho local: `C:\tools\toolbox-plugins`
- Repositório remoto: https://github.com/rodrigolessadev/toolbox-plugins
- Branch atual: main
- Último commit: a745a00 (HEAD -> main) atualizações na funcionalidade
- Estado Git:
- Linguagem principal:
- Framework ou runtime:
- Ferramentas de validação:
- Diretórios principais:
  - `.claude`
  - `.code-review-graph`
  - `.codebuddy`
  - `.gemini`
  - `.github`
  - `.Issues`
  - `.kiro`
  - `.pytest_cache`
  - `.qoder`
  - `.vscode`
  - `graphify-out`
  - `plugins`
  - `_shared`
- Arquivos de configuração:
- Testes:
- Formato dos plugins:
- Catálogo:
- Riscos identificados:
- Pendências:

- Diretórios de código:
  - plugins
  - _shared

- Diretórios de suporte ao desenvolvimento:
  - .github
  - .Issues

- Diretórios de análise e automação:
  - .code-review-graph
  - graphify-out

- Diretórios de configuração de ferramentas:
  - .claude
  - .codebuddy
  - .gemini
  - .kiro
  - .qoder
  - .vscode

- Diretórios de testes:
  - Não foram identificados diretórios de testes próprios do projeto nesta etapa.
  - A presença de .pytest_cache indica utilização ou execução prévia do 

## Relações entre os projetos

- Contrato de comunicação:
- Formato dos metadados:
- Processo de instalação:
- Processo de empacotamento:
- Compatibilidade entre versões:
- Arquivos compartilhados:
- Dependências entre os projetos:

## Observações gerais

- Este inventário deve ser atualizado quando a estrutura de qualquer projeto mudar.
- Nenhuma conclusão arquitetural deve ser considerada definitiva apenas com base
  neste documento.
- Informações desconhecidas devem ser marcadas como `A confirmar`.
