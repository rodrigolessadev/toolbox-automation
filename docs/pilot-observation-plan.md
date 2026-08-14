# Plano de observação da tarefa-piloto

## Objetivo

Acompanhar a primeira execução e registrar evidências suficientes para
identificar falhas de processo, excesso de permissão ou inconsistências entre
as etapas.

## Pontos de observação

### Recebimento

Verificar:

- task_id criado;
- título e descrição preservados;
- risco classificado;
- repositório identificado;
- status inicial correto.

### Contexto

Verificar:

- arquivos de contexto carregados;
- handoff consultado;
- decisões relevantes identificadas;
- status dos testes consultado;
- inventário disponível.

### Estado Git

Registrar:

- branch;
- commit atual;
- arquivos modificados;
- arquivos não rastreados;
- conflitos;
- divergência remota, quando disponível.

### Análise

Verificar:

- arquivos relacionados localizados;
- escopo documentado;
- dependências identificadas;
- riscos registrados;
- arquivos protegidos excluídos.

### Planejamento

Verificar:

- etapas ordenadas;
- arquivos previstos;
- testes definidos;
- critérios de sucesso;
- rollback definido;
- aprovações identificadas.

### Implementação

Verificar:

- somente arquivos aprovados foram alterados;
- nenhuma alteração local foi descartada;
- comandos executados foram registrados;
- checkpoint atualizado;
- alterações inesperadas interromperam o fluxo.

### Validação

Verificar:

- testes executados;
- códigos de retorno preservados;
- falhas registradas;
- diff revisado;
- segredos não expostos;
- escopo confirmado.

### Encerramento

Verificar:

- resultado final produzido;
- riscos remanescentes informados;
- próxima ação registrada;
- handoff atualizado;
- nenhum bloqueio foi omitido.

## Evidências

Registrar somente informações não sensíveis:

- task request;
- checkpoint;
- resultado dos testes;
- resumo do diff;
- lista de arquivos;
- decisões;
- bloqueios;
- aprovações.

Não registrar:

- tokens;
- senhas;
- chaves;
- cookies;
- dados pessoais;
- conteúdo integral de arquivos protegidos.
