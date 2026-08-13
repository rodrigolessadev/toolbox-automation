# Agentes da Toolbox Automation Platform

## Objetivo

Os agentes especializados dividem as responsabilidades de análise,
implementação, validação, revisão e release dos projetos Toolbox.

Cada agente possui:

- uma responsabilidade principal;
- permissões específicas;
- entradas esperadas;
- saída estruturada;
- critérios de bloqueio;
- agente seguinte no fluxo.

## Agentes

| Agente | Arquivo | Responsabilidade |
|---|---|---|
| Orquestrador | `orchestrator.md` | Coordenar o fluxo completo |
| Analista | `analyst.md` | Analisar arquitetura e impacto |
| Implementador | `implementer.md` | Implementar alterações aprovadas |
| Testador | `tester.md` | Criar e executar validações |
| Revisor visual | `visual-reviewer.md` | Revisar interface e evidências visuais |
| Revisor de segurança | `security-reviewer.md` | Identificar riscos de segurança |
| Gerente de release | `release-manager.md` | Preparar entrega e ações externas |

## Fluxo padrão


## Regras

- Um agente não deve assumir a responsabilidade de outro.
- O implementador só atua após existir um plano aprovado.
- O gerente de release só prepara ações externas.
- Push, pull request, merge, release e deploy exigem aprovação humana.
- O orquestrador deve bloquear tarefas com saída inválida ou escopo inconsistente.
- Toda saída deve utilizar o schema correspondente.
