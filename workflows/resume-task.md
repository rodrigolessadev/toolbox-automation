# Workflow: retomar tarefa interrompida

## Identificação

- Nome: `resume-task`
- Finalidade: retomar uma tarefa existente com segurança
- Schema principal: `checkpoint.schema.json`

## Quando utilizar

Utilizar este workflow quando:

- houver um checkpoint existente;
- a sessão anterior tiver sido interrompida;
- existir um `handoff.md` com tarefa pendente;
- uma tarefa estiver marcada como `in_progress`;
- uma tarefa estiver bloqueada e houver nova informação;
- o usuário solicitar a retomada de uma tarefa anterior.

## Entradas

- `task_id`;
- checkpoint existente;
- `.agent/handoff.md`;
- resultado parcial da implementação;
- resultado parcial dos testes;
- estado atual dos repositórios;
- decisões registradas;
- aprovação anterior, se existente.

## Agentes envolvidos

1. Orquestrador;
2. Analista;
3. Implementador, se a implementação estiver incompleta;
4. Testador;
5. Revisores aplicáveis;
6. Gerente de release.

## Fases

### Fase 1 — Localizar o estado anterior

O orquestrador deverá:

- localizar o checkpoint;
- confirmar o `task_id`;
- identificar a fase interrompida;
- listar fases concluídas;
- listar ações pendentes;
- listar bloqueios;
- identificar repositórios modificados;
- identificar arquivos modificados.

Se não for possível localizar o estado anterior, o workflow deverá ser bloqueado.

### Fase 2 — Verificar alterações atuais

Antes de continuar:

- consultar o estado Git;
- comparar o estado atual com o checkpoint;
- identificar alterações feitas desde a última atualização;
- preservar alterações locais;
- verificar se o branch continua correto;
- verificar se o escopo continua válido.

Se houver alterações inesperadas, parar e solicitar orientação.

### Fase 3 — Revalidar o escopo

O orquestrador deverá confirmar:

- se os mesmos repositórios continuam envolvidos;
- se os arquivos continuam autorizados;
- se o risco mudou;
- se a aprovação anterior continua válida;
- se novos arquivos foram incluídos;
- se surgiram dependências novas.

Se o escopo tiver mudado, a aprovação anterior deverá ser considerada expirada.

### Fase 4 — Retomar a fase pendente

Executar somente a próxima ação indicada no checkpoint.

Exemplos:

- continuar a implementação;
- executar os testes pendentes;
- corrigir uma falha;
- realizar uma revisão;
- atualizar a documentação;
- preparar a entrega.

O workflow não deve repetir automaticamente fases já concluídas sem motivo documentado.

### Fase 5 — Validar novamente

Após a retomada:

- executar as validações pendentes;
- verificar o diff;
- verificar o escopo;
- executar varredura de segredos;
- confirmar compatibilidade;
- atualizar os resultados estruturados.

### Fase 6 — Atualizar o checkpoint

Registrar:

- fase atual;
- fases concluídas;
- ações pendentes;
- bloqueios;
- arquivos modificados;
- próxima ação;
- data da atualização;
- aprovações válidas.

### Fase 7 — Encerrar

O workflow poderá produzir:

- `completed`;
- `completed_with_warnings`;
- `blocked`;
- `failed`;
- `cancelled`.

## Deve bloquear quando

- não houver checkpoint confiável;
- o `task_id` não puder ser confirmado;
- o estado Git divergir de forma inesperada;
- a aprovação anterior tiver expirado;
- houver arquivo fora do escopo;
- houver segredo no diff;
- existirem conflitos não resolvidos;
- a próxima ação não estiver clara.

## Estratégia de rollback

Não executar rollback destrutivo automaticamente.

Preservar:

- alterações existentes;
- diffs;
- registros;
- checkpoints;
- resultados parciais.

Qualquer descarte deverá ser aprovado especificamente pelo usuário.
