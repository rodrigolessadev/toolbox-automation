# Políticas da Toolbox Automation Platform

## Objetivo

Este diretório contém as regras de permissão, aprovação, acesso a arquivos,
bloqueio e execução de ações externas da plataforma de automação.

As políticas devem ser interpretadas conjuntamente com:

- `docs/automation-scope.md`;
- `.agent/project-context.md`;
- `.agent/decisions.md`;
- `agents/`;
- `schemas/`.

## Princípios

- menor privilégio;
- escopo explícito;
- aprovação humana para ações sensíveis;
- separação entre implementação e revisão;
- rastreabilidade;
- reversibilidade sempre que possível;
- nenhuma ação externa sem autorização;
- parada segura diante de ambiguidade.

## Políticas

| Arquivo | Finalidade |
|---|---|
| `permission-levels.md` | Define os níveis de permissão |
| `approval-policy.md` | Define quando solicitar aprovação |
| `blocked-actions.md` | Lista ações proibidas |
| `file-access-policy.md` | Controla acesso a arquivos e diretórios |
| `external-actions-policy.md` | Controla GitHub, publicação e deploy |
| `ui-design-guidelines.md` | Diretrizes de UI, contraste, temas e coerência contextual de ícones |
| `database-persistence-policy.md` | Regra mandatória de persistência no SQLite Central (Abordagem B) |

## Regra de precedência

Em caso de conflito entre regras, aplicar a mais restritiva.

A automação nunca deve interpretar uma permissão implícita como autorização
para executar uma ação sensível.
