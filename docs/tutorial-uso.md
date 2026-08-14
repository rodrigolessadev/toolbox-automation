# Tutorial de Uso — Toolbox Automation Platform

Guia prático e passo a passo para utilizar a automação com os repositórios **Toolbox** e **Toolbox Plugins**.

---

## 1. Visão Geral da Estrutura

A plataforma de automação gerencia o fluxo de trabalho entre três projetos:

1. **`toolbox-automation`** (`C:\tools\toolbox-automation`): Orquestração, políticas, checkpoints, testes e agentes.
2. **`toolbox`** (`C:\tools\toolbox`): Aplicação desktop principal (Tauri/Rust + Frontend).
3. **`toolbox-plugins`** (`C:\tools\toolbox-plugins`): Repositório do ecossistema de plugins, metadados e empacotamento (`catalog.json`).

---

## 2. Configuração Inicial

### 2.1 Criar a Configuração Local

O arquivo `config/local-projects.yaml` define os caminhos e permissões locais na sua máquina (este arquivo não é versionado).

Copie o modelo de exemplo para criar o seu:

```powershell
Copy-Item config\local-projects.example.yaml config\local-projects.yaml
```

Certifique-se de que o arquivo `config/local-projects.yaml` aponta para os diretórios corretos:

```yaml
version: 1

projects:
  toolbox-automation:
    path: "C:/tools/toolbox-automation"
    role: automation
    required: true

  toolbox:
    path: "C:/tools/toolbox"
    role: product
    required: true

  toolbox-plugins:
    path: "C:/tools/toolbox-plugins"
    role: plugins
    required: true

authorized_roots:
  - "C:/tools/toolbox-automation"
  - "C:/tools/toolbox"
  - "C:/tools/toolbox-plugins"

protected_patterns:
  - "**/.env"
  - "**/.env.*"
  - "**/*.key"
  - "**/*.pem"
  - "**/*.p12"
  - "**/*.pfx"
  - "**/secrets/**"
  - "**/credentials/**"

local_only:
  - config/local-projects.yaml
  - ".agent/local/**"
  - ".agent/runtime/**"
  - ".agent/checkpoints/**"

validation:
  check_git_repository: true
  check_clean_start: false
  check_required_files: true
  check_protected_paths: true
```

### 2.2 Configuração do Graphify (Opcional)

Para habilitar a camada de análise estrutural somente leitura:

```powershell
Copy-Item config\graphify.example.yaml config\graphify.yaml
```

---

## 3. Inicialização e Verificação de Integridade

Sempre antes de iniciar qualquer trabalho, execute os procedimentos de verificação de ambiente:

### Passo 1: Verificar os projetos locais
```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-projects.ps1
```
*O script valida a existência física das três pastas e confirma se são repositórios Git válidos.*

### Passo 2: Carregar a memória de contexto
```powershell
powershell -ExecutionPolicy Bypass -File scripts/load-context.ps1
```
*Opcional: Passe `-WithGraph` para verificar a disponibilidade de grafos de dependência em modo somente leitura.*

---

## 4. Executando os Testes de Avaliação (`evals/`)

A suíte de testes valida a conformidade das políticas, schemas, fluxos, scripts de automação e governança.

Execute os testes de validação em modo somente leitura:

```powershell
# Validar schemas JSON
powershell -ExecutionPolicy Bypass -File evals/test-schemas.ps1

# Validar workflows
powershell -ExecutionPolicy Bypass -File evals/test-workflows.ps1

# Validar políticas de segurança
powershell -ExecutionPolicy Bypass -File evals/test-policies.ps1

# Validar caminhos protegidos
powershell -ExecutionPolicy Bypass -File evals/test-protected-paths.ps1

# Validar scripts operacionais
powershell -ExecutionPolicy Bypass -File evals/test-scripts.ps1

# Validar configurações
powershell -ExecutionPolicy Bypass -File evals/test-config.ps1

# Validar governança e isolamento do Graphify
powershell -ExecutionPolicy Bypass -File evals/test-graphify.ps1
```

---

## 5. Análise de Dependências e Impacto com Graphify (Opcional)

O Graphify fornece suporte analítico passivo para identificar dependências antes de alterar código:

- **Análise de Impacto de um Arquivo (Somente Leitura)**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -ImpactAnalysis -TargetFile "scripts/load-context.ps1"
  ```
- **Geração de Grafo Derivado (Exige flag explícita)**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -BuildGraph
  ```
- **Regras de Governança**: Consulte [`policies/graphify-policy.md`](file:///c:/tools/toolbox-automation/policies/graphify-policy.md).

---

## 6. Ciclo de Vida de uma Tarefa (Passo a Passo)

```
 [Recepção] ──► [Análise] ──► [Plano] ──► [Aprovação] ──► [Implementação] ──► [Validação] ──► [Revisão] ──► [Release]
```

### Etapa 1: Iniciar uma Nova Tarefa (Manual ou via Issue do Kanban)

#### Opção A — Disparo Automático a partir de uma Issue do GitHub / Kanban:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/init-task-from-issue.ps1 -Repo "toolbox-plugins" -IssueNumber 4
```

#### Opção B — Início Manual:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-task.ps1 -TaskId "TASK-105" -Description "Implementar novo recurso no Toolbox"
```

### Etapa 2: Executar as Fases com os Agentes

1. **Analista (`agents/analyst.md`)**: Analisa o impacto nos repositórios sem alterar código.
2. **Orquestrador (`agents/orchestrator.md`)**: Cria o plano técnico detalhado.
3. **Humano**: Revisa e aprova o plano de implementação.
4. **Implementador (`agents/implementer.md`)**: Realiza apenas as alterações autorizadas dentro do escopo.
5. **Testador (`agents/tester.md`)**: Executa suítes de testes unitários e de integração.
6. **Revisores Especializados (`agents/security-reviewer.md`, `agents/visual-reviewer.md`)**: Avaliam conformidade e segurança.
7. **Release Manager (`agents/release-manager.md`)**: Consolida a entrega e atualiza o histórico.

### Etapa 3: Retomada Segura de Tarefas Interrompidas

```powershell
powershell -ExecutionPolicy Bypass -File scripts/resume-task.ps1 -TaskId "TASK-105"
```

---

## 7. Workflows Disponíveis

| Workflow | Quando Utilizar | Arquivo de Referência |
|---|---|---|
| **Nova Funcionalidade** | Desenvolvimento de novos recursos na aplicação | [`workflows/new-feature.md`](file:///c:/tools/toolbox-automation/workflows/new-feature.md) |
| **Ciclo de Vida de Plugin** | Criação, atualização ou publicação de plugins | [`workflows/plugin-lifecycle.md`](file:///c:/tools/toolbox-automation/workflows/plugin-lifecycle.md) |
| **Correção de Bugs** | Investigação e correção pontual de falhas | [`workflows/bug-fix.md`](file:///c:/tools/toolbox-automation/workflows/bug-fix.md) |
| **Manutenção Preventiva** | Auditorias, refatorações e atualizações de dependências | [`workflows/preventive-maintenance.md`](file:///c:/tools/toolbox-automation/workflows/preventive-maintenance.md) |
| **Retomada de Tarefa** | Recuperação de fluxo a partir de checkpoints salvos | [`workflows/resume-task.md`](file:///c:/tools/toolbox-automation/workflows/resume-task.md) |

---

## 8. Integração com o Plugin Release e Kanban

O plugin localizado em `C:\tools\toolbox-plugins\plugins\release` facilita a operação diária:

### 1. Aba Projeto (Kanban / Project Board V2)
- **Criar Issues**: Permite criar issues com tags `tipo: feature` ou `tipo: bug` no repositório correto.
- **Iniciar Desenvolvimento**: Move a issue para `🚀 Em andamento` e cria/faz checkout na branch `feature/<slug>`.
- **Revisão e Conclusão**: Detecta automaticamente `Closes #N` no commit para mover para `🔍 Em revisão` e `✅ Concluído`.

### 2. Aba Toolbox (Release da Aplicação)
- Atualiza a versão no `Cargo.toml`/`package.json`.
- Cria a tag Git `vX.Y.Z` e faz o push para o GitHub.
- Dispara a GitHub Action com Tauri para gerar o instalador `.exe`/`.msi`.

### 3. Aba Marketplace (Release de Plugins)
- Atualiza `plugins/<id>/plugin.json` e o `catalog.json`.
- Cria a tag Git `<id>-<versao>` e faz push.
- Dispara a GitHub Action para empacotar o ZIP e anexar ao GitHub Release.

---

## 9. Políticas de Segurança e Boas Práticas

- **Princípio do Menor Privilégio**: Leituras e análises não alteram arquivos.
- **Preservação de Alterações Locais**: A automação nunca executa `git reset --hard` ou `git clean -fd` automaticamente.
- **Arquivos Protegidos**: Arquivos `.env`, chaves `.pem`/`.key` e credenciais são bloqueados por padrão através de `config/protected-paths.yaml`.
- **Aprovações Explícitas**: Operações de `git push`, criação de tags remotas, releases e deploy exigem confirmação humana.
