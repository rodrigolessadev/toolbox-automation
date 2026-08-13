# MCPs e integrações da Toolbox Automation Platform

## Objetivo

Este diretório documenta as ferramentas e integrações que poderão ser usadas
pelos agentes da automação.

A documentação define:

- finalidade;
- agentes autorizados;
- operações permitidas;
- operações bloqueadas;
- nível de permissão;
- necessidade de aprovação;
- dados que não podem ser enviados;
- comportamento esperado em caso de falha.

## MCPs documentados

| Arquivo | Integração |
|---|---|
| `files-code.md` | Arquivos e código |
| `graphify.md` | Graphify |
| `github.md` | GitHub |
| `controlled-execution.md` | Execução controlada |
| `browser.md` | Navegador |
| `documentation.md` | Documentação técnica |
| `permissions-matrix.md` | Matriz de permissões |

## Princípios

- menor privilégio;
- acesso somente dentro do escopo;
- separação entre leitura e alteração;
- aprovação para ações externas;
- proteção de segredos;
- registro de operações relevantes;
- parada segura diante de falhas;
- nenhum fallback que amplie permissões.

## Regra de precedência

As políticas em `policies/` têm precedência sobre esta documentação.

Quando uma ferramenta permitir uma operação, mas a política da automação
proibir essa operação, a política mais restritiva deverá ser aplicada.

## Regra de indisponibilidade

Se um MCP necessário estiver indisponível:

1. registrar a indisponibilidade;
2. informar o impacto;
3. verificar se existe alternativa segura;
4. não substituir automaticamente por uma ferramenta de maior privilégio;
5. bloquear a tarefa se a ferramenta for obrigatória.
