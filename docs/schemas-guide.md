# Guia dos schemas da automação

## Objetivo

Os schemas definem os contratos estruturados utilizados pelos agentes,
workflows e checkpoints da Toolbox Automation Platform.

Eles evitam respostas inconsistentes e permitem validar automaticamente os
resultados produzidos durante uma tarefa.

## Fluxo dos contratos

Durante todo o processo, o estado persistente deve ser registrado em:

- `.agent/checkpoints/<task_id>.json` (conforme `checkpoint.schema.json`)
- `.agent/work-log.md`
- `.agent/handoff.md`

## Regras

1. Todo workflow deve possuir um `task_id`.
2. O `task_id` deve permanecer o mesmo durante toda a execução.
3. Agentes não devem inventar campos fora do schema.
4. Campos desconhecidos devem ser documentados como `A confirmar`.
5. Uma tarefa bloqueada não pode ser considerada concluída.
6. Uma validação não executada não pode ser registrada como aprovada.
7. Alterações fora do escopo devem bloquear o workflow.
8. Aprovações pendentes devem aparecer no resultado final.
9. O checkpoint deve ser atualizado após cada fase importante.
10. Resultados parciais devem ser preservados quando houver interrupção.

## Estados

Os estados disponíveis estão definidos nos schemas e devem ser usados de
forma consistente:

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

Um workflow só pode produzir o estado `completed` quando:

- a implementação terminou;
- o escopo foi respeitado;
- as validações obrigatórias foram executadas;
- não existem bloqueios;
- as revisões necessárias foram concluídas;
- as aprovações externas pendentes foram identificadas;
- o checkpoint foi atualizado.
