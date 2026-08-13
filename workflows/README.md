# Workflows da Toolbox Automation Platform

## Objetivo

Este diretório contém os fluxos operacionais utilizados pela automação para
receber, analisar, implementar, testar, revisar e preparar tarefas.

## Workflows disponíveis

| Workflow | Finalidade |
|---|---|
| `resume-task.md` | Retomar tarefa interrompida |
| `new-feature.md` | Implementar novo recurso |
| `plugin-lifecycle.md` | Criar ou atualizar plugin |
| `bug-fix.md` | Corrigir falha |
| `preventive-maintenance.md` | Executar manutenção preventiva |

## Estrutura obrigatória

Todo workflow deve definir:

- objetivo;
- quando utilizar;
- entradas;
- agentes envolvidos;
- fases;
- critérios de aprovação;
- critérios de bloqueio;
- validações;
- checkpoint;
- resultado final;
- estratégia de rollback.

## Estados possíveis

Os workflows utilizam os estados definidos nos schemas:

- `draft`;
- `planned`;
- `approved`;
- `in_progress`;
- `blocked`;
- `validation`;
- `completed`;
- `failed`;
- `cancelled`.

## Regra de conclusão

Um workflow só poderá ser marcado como concluído quando:

- a implementação estiver registrada;
- o escopo tiver sido respeitado;
- os testes obrigatórios forem avaliados;
- as revisões aplicáveis forem concluídas;
- não houver bloqueios;
- as aprovações pendentes estiverem identificadas;
- o checkpoint estiver atualizado.

## Regra de segurança

Nenhum workflow pode executar automaticamente:

- `git push`;
- pull request;
- merge;
- release;
- deploy;
- publicação de pacote;
- descarte de alterações locais;
- ações destrutivas.
