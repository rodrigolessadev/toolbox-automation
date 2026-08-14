# Tarefa-piloto da Toolbox Automation Platform

## Identificação

- Task ID: `TASK-101`
- Nome: validação controlada da automação
- Tipo: `new-feature` ou `bug-fix`
- Repositório: `toolbox-automation`
- Risco: baixo
- Status inicial: `draft`
- Responsável: Rodrigo

## Objetivo

Validar o fluxo operacional da automação em uma alteração pequena, local,
reversível e sem ações externas.

## Escopo permitido

A tarefa poderá modificar somente:

- documentação previamente definida;
- registros de checkpoint;
- testes estruturais, se necessário;
- um único arquivo adicional aprovado durante o planejamento.

## Escopo proibido

A tarefa não poderá:

- alterar `toolbox`;
- alterar `toolbox-plugins`;
- alterar contratos públicos;
- instalar dependências;
- acessar arquivos protegidos;
- executar ações externas;
- fazer `git push`;
- criar pull request;
- fazer merge;
- publicar release;
- executar deploy;
- descartar alterações locais;
- executar comandos destrutivos.

## Critérios de sucesso

- o task request for criado;
- o contexto persistente for carregado;
- o estado Git inicial for registrado;
- a análise for concluída;
- o plano for criado;
- a aprovação humana for registrada;
- a implementação respeitar o escopo;
- os testes obrigatórios forem executados;
- o diff for revisado;
- o checkpoint for atualizado;
- o resultado final for produzido;
- nenhuma ação externa for realizada.

## Critérios de bloqueio

Bloquear a tarefa quando:

- o repositório não puder ser identificado;
- houver alterações locais inesperadas;
- surgir arquivo fora do escopo;
- forem necessários comandos não aprovados;
- houver necessidade de acesso externo;
- forem encontrados dados sensíveis;
- os testes obrigatórios falharem;
- o plano aprovado deixar de refletir a implementação;
- surgir uma dependência nova.

## Rollback

O rollback deverá ser somente local e não destrutivo.

Priorizar:

- preservação do diff;
- restauração manual de arquivo específico;
- reversão de commit local, se houver;
- manutenção dos registros e checkpoints.

Não executar `git reset --hard`, `git clean -fd` ou comandos equivalentes.

## Resultado esperado

A tarefa deverá terminar com um relatório contendo:

- resumo;
- arquivos alterados;
- testes;
- revisões;
- bloqueios;
- riscos;
- aprovações;
- próxima ação.
