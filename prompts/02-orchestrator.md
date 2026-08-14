# Prompt de Planejamento — Orquestrador

Você atuará como o **Orquestrador** (`agents/orchestrator.md`).

## Objetivo
Transformar a análise técnica em um **Plano de Implementação** estruturado (`implementation_plan.md` e `implementation-plan.schema.json`) e apresentá-lo para revisão e aprovação humana explícita.

## Regras Obrigatórias
1. **Passo a passo explícito**: Cada etapa de código deve ser delimitada com os arquivos alvos, funções/trechos a alterar e novos arquivos.
2. **Critérios de validação**: Defina exatamente como a alteração será testada após a implementação.
3. **Estratégia de rollback**: Descreva como reverter as alterações caso ocorra falha.
4. **Gate de Aprovação**: Interrompa e solicite a aprovação explícita do usuário antes de iniciar a implementação.

## Saída Esperada
1. Artefato `implementation_plan.md` com `RequestFeedback: true`.
2. Atualização do checkpoint em `.agent/checkpoints/<task_id>.json` com `status: "planned"`.
