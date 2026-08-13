# Guia dos agentes da automação

## Princípio central

Cada agente possui uma responsabilidade específica. A divisão existe para
reduzir erros, separar implementação de revisão e manter as ações sensíveis
sob controle humano.

## Fluxo padrão

### 1. Recebimento

O orquestrador recebe uma solicitação no formato definido por
`task-request.schema.json`.

### 2. Análise

O analista investiga a arquitetura, os arquivos afetados, as dependências e
os riscos. Nenhum código de produto deve ser alterado nessa fase.

### 3. Planejamento

O orquestrador transforma a análise em um plano de implementação com:

- etapas;
- arquivos;
- testes;
- aprovações;
- critérios de sucesso;
- estratégia de rollback.

### 4. Aprovação

A aprovação é necessária quando houver:

- alteração sensível;
- dependência nova;
- alteração nos dois repositórios;
- alteração de contrato;
- ação destrutiva;
- ação externa.

### 5. Implementação

O implementador executa somente o plano aprovado.

### 6. Validação

O testador executa os testes e registra os resultados. Uma validação não
executada não pode ser marcada como aprovada.

### 7. Revisões especializadas

As revisões são acionadas conforme o tipo de alteração:

| Alteração | Revisão |
|---|---|
| Interface ou tema | Visual |
| Executor, instalador ou comandos | Segurança |
| Dependências | Segurança |
| Contrato entre projetos | Compatibilidade e arquitetura |
| Documentação | Documentação |
| Código em geral | Código |

### 8. Preparação da entrega

O gerente de release revisa o estado final, prepara o resumo e lista as
aprovações que ainda dependem do usuário.

## Regras de independência

- O implementador não aprova a própria implementação.
- O testador não corrige código de produção.
- O revisor de segurança não altera silenciosamente o diff.
- O gerente de release não executa publicação sem aprovação.
- O orquestrador não deve mascarar bloqueios.

## Regra de parada

Qualquer agente deve interromper a execução quando:

- a solicitação for ambígua;
- o escopo estiver incompleto;
- houver conflito local;
- houver segredo;
- houver arquivo inesperado;
- houver risco crítico;
- a saída não puder ser validada;
- uma ação externa for necessária sem aprovação.

## Critério de sucesso

Um fluxo de agentes só pode ser considerado concluído quando:

- a implementação estiver registrada;
- os testes obrigatórios forem avaliados;
- as revisões aplicáveis estiverem concluídas;
- o escopo tiver sido respeitado;
- os riscos remanescentes estiverem documentados;
- as aprovações pendentes estiverem explícitas;
- o checkpoint estiver atualizado.
