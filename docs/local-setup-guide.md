# Guia de configuração local

## Objetivo

Este documento explica como configurar a automação para trabalhar com os
três repositórios autorizados e utilizar recursos analíticos opcionais como o Graphify.

## Repositórios esperados

- `toolbox-automation`
- `toolbox`
- `toolbox-plugins`

## Configuração local

A configuração real dos projetos locais deve estar em:

- `config/local-projects.yaml` (baseado em `config/local-projects.example.yaml`)

Para habilitar a integração analítica opcional com o Graphify:

- `config/graphify.yaml` (baseado em `config/graphify.example.yaml`)

## Inicialização

Executar, nesta ordem:

1. `powershell -ExecutionPolicy Bypass -File scripts/check-projects.ps1`
2. `powershell -ExecutionPolicy Bypass -File scripts/load-context.ps1`
3. *(Opcional)* `powershell -ExecutionPolicy Bypass -File scripts/load-context.ps1 -WithGraph`

A inicialização deve ser interrompida quando:

- um repositório não existir;
- um diretório não for um repositório Git;
- o contexto persistente estiver incompleto;
- a configuração local estiver ausente.

## Uso do Graphify (Opcional e Somente Leitura)

O Graphify atua como camada de análise estrutural e não é obrigatório para nenhuma tarefa.

- **Análise de Impacto de um Arquivo**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -ImpactAnalysis -TargetFile "scripts/load-context.ps1"
  ```
- **Geração do Grafo Local**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -BuildGraph
  ```
*Nota: A ferramenta nunca instala dependências automaticamente e não indexa arquivos protegidos como `.env` ou chaves privadas.*

## Criar uma tarefa

Exemplo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-task.ps1 -TaskId "TASK-102" -Description "Descrição da tarefa"
```

## Regras de segurança

- não adicionar credenciais à configuração;
- não descartar alterações locais;
- não executar comandos destrutivos;
- não fazer push automaticamente;
- não iniciar implementação sem plano aprovado;
- não ignorar arquivos protegidos;
- não utilizar caminhos fora dos diretórios autorizados.
